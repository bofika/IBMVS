"""
Interactive features panel (chat, polls, Q&A).
"""
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QComboBox, QGroupBox, QCheckBox, QSpinBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox,
    QListWidget, QTextEdit
)
from PyQt6.QtCore import Qt

from ui.base_panel import BasePanel
from api.interactivity import interactivity_manager
from api.channels import channel_manager
from core.logger import get_logger
from core.exceptions import NotFoundError

logger = get_logger(__name__)


class CreatePollDialog(QDialog):
    """Dialog for creating a poll."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Poll")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup dialog UI."""
        layout = QVBoxLayout(self)
        
        # Form
        form = QFormLayout()
        
        # Question
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("Enter poll question")
        form.addRow("Question:", self.question_input)
        
        # Duration
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(0, 3600)
        self.duration_spin.setValue(300)
        self.duration_spin.setSuffix(" seconds")
        self.duration_spin.setSpecialValueText("No limit")
        form.addRow("Duration:", self.duration_spin)
        
        layout.addLayout(form)
        
        # Options
        options_label = QLabel("Poll Options (2-10):")
        layout.addWidget(options_label)
        
        self.options_list = QListWidget()
        layout.addWidget(self.options_list)
        
        # Add/Remove option buttons
        option_buttons = QHBoxLayout()
        
        add_option_btn = QPushButton("Add Option")
        add_option_btn.clicked.connect(self.add_option)
        option_buttons.addWidget(add_option_btn)
        
        remove_option_btn = QPushButton("Remove Selected")
        remove_option_btn.clicked.connect(self.remove_option)
        option_buttons.addWidget(remove_option_btn)
        
        option_buttons.addStretch()
        layout.addLayout(option_buttons)
        
        # Add default options
        self.add_option("Option 1")
        self.add_option("Option 2")
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def add_option(self, text: str = ""):
        """Add a poll option."""
        if self.options_list.count() >= 10:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Limit Reached", "Maximum 10 options allowed.")
            return
        
        if not text:
            text = f"Option {self.options_list.count() + 1}"
        
        self.options_list.addItem(text)
        
        # Make item editable
        item = self.options_list.item(self.options_list.count() - 1)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
    
    def remove_option(self):
        """Remove selected option."""
        current_row = self.options_list.currentRow()
        if current_row >= 0:
            self.options_list.takeItem(current_row)
    
    def get_poll_data(self):
        """Get poll data."""
        options = []
        for i in range(self.options_list.count()):
            options.append(self.options_list.item(i).text())
        
        duration = self.duration_spin.value() if self.duration_spin.value() > 0 else None
        
        return {
            'question': self.question_input.text().strip(),
            'options': options,
            'duration': duration
        }


class InteractivePanel(BasePanel):
    """Panel for managing interactive features."""
    
    def __init__(self):
        super().__init__("Interactive Features")
        self.current_channel_id = None
    
    def setup_ui(self):
        """Setup the interactive features panel UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Interactive Features")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title_label)
        
        # Channel selector
        channel_layout = QHBoxLayout()
        channel_layout.addWidget(QLabel("Channel:"))
        
        self.channel_combo = QComboBox()
        self.channel_combo.currentIndexChanged.connect(self.on_channel_changed)
        self.load_channels()
        channel_layout.addWidget(self.channel_combo)
        channel_layout.addStretch()
        
        layout.addLayout(channel_layout)
        
        # Chat Settings Group
        chat_group = QGroupBox("Chat Settings")
        chat_layout = QFormLayout()
        
        self.chat_enabled_check = QCheckBox()
        chat_layout.addRow("Enable Chat:", self.chat_enabled_check)
        
        self.chat_moderation_combo = QComboBox()
        self.chat_moderation_combo.addItems(["auto", "manual", "off"])
        chat_layout.addRow("Moderation:", self.chat_moderation_combo)
        
        self.chat_require_login_check = QCheckBox()
        chat_layout.addRow("Require Login:", self.chat_require_login_check)
        
        self.chat_slow_mode_check = QCheckBox()
        chat_layout.addRow("Slow Mode:", self.chat_slow_mode_check)
        
        self.chat_slow_interval_spin = QSpinBox()
        self.chat_slow_interval_spin.setRange(0, 60)
        self.chat_slow_interval_spin.setValue(5)
        self.chat_slow_interval_spin.setSuffix(" seconds")
        chat_layout.addRow("Slow Mode Interval:", self.chat_slow_interval_spin)
        
        save_chat_btn = QPushButton("Save Chat Settings")
        save_chat_btn.clicked.connect(self.save_chat_settings)
        chat_layout.addRow("", save_chat_btn)
        
        chat_group.setLayout(chat_layout)
        layout.addWidget(chat_group)
        
        # Polls Group
        polls_group = QGroupBox("Polls")
        polls_layout = QVBoxLayout()
        
        # Polls toolbar
        polls_toolbar = QHBoxLayout()
        
        create_poll_btn = QPushButton("Create Poll")
        create_poll_btn.clicked.connect(self.create_poll)
        polls_toolbar.addWidget(create_poll_btn)
        
        refresh_polls_btn = QPushButton("Refresh")
        refresh_polls_btn.clicked.connect(self.load_polls)
        polls_toolbar.addWidget(refresh_polls_btn)
        
        polls_toolbar.addStretch()
        polls_layout.addLayout(polls_toolbar)
        
        # Polls table
        self.polls_table = QTableWidget()
        self.polls_table.setColumnCount(4)
        self.polls_table.setHorizontalHeaderLabels([
            "ID", "Question", "Status", "Actions"
        ])
        self.polls_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        polls_layout.addWidget(self.polls_table)
        
        polls_group.setLayout(polls_layout)
        layout.addWidget(polls_group)
        
        # Q&A Settings Group
        qa_group = QGroupBox("Q&A Settings")
        qa_layout = QFormLayout()
        
        self.qa_enabled_check = QCheckBox()
        qa_layout.addRow("Enable Q&A:", self.qa_enabled_check)
        
        self.qa_moderation_check = QCheckBox()
        qa_layout.addRow("Enable Moderation:", self.qa_moderation_check)
        
        save_qa_btn = QPushButton("Save Q&A Settings")
        save_qa_btn.clicked.connect(self.save_qa_settings)
        qa_layout.addRow("", save_qa_btn)
        
        qa_group.setLayout(qa_layout)
        layout.addWidget(qa_group)
        
        # Add stretch
        layout.addStretch()
    
    def load_channels(self):
        """Load channels into combo box."""
        try:
            response = channel_manager.list_channels()
            channels = response.get('channels', [])
            
            self.channel_combo.clear()
            for channel in channels:
                self.channel_combo.addItem(
                    channel.get('title', 'Untitled'),
                    channel.get('id')
                )
            
            if channels:
                self.current_channel_id = channels[0].get('id')
                self.load_settings()
        except Exception as e:
            self.show_error(f"Failed to load channels: {str(e)}")
    
    def on_channel_changed(self, index: int):
        """Handle channel selection change."""
        if index >= 0:
            self.current_channel_id = self.channel_combo.currentData()
            self.load_settings()
    
    def load_settings(self):
        """Load all interactive settings."""
        self.load_chat_settings()
        self.load_polls()
        self.load_qa_settings()
    
    def load_chat_settings(self):
        """Load chat settings."""
        if not self.current_channel_id:
            return
        
        if not hasattr(self, 'chat_enabled_check'):
            logger.warning("Chat settings UI not initialized yet")
            return
        
        try:
            settings = interactivity_manager.get_chat_settings(self.current_channel_id)
            
            self.chat_enabled_check.setChecked(settings.get('enabled', False))
            
            moderation = settings.get('moderation', 'auto')
            index = self.chat_moderation_combo.findText(moderation)
            if index >= 0:
                self.chat_moderation_combo.setCurrentIndex(index)
            
            self.chat_require_login_check.setChecked(settings.get('require_login', False))
            self.chat_slow_mode_check.setChecked(settings.get('slow_mode', False))
            self.chat_slow_interval_spin.setValue(settings.get('slow_mode_interval', 5))
            
            logger.info(f"Loaded chat settings for channel {self.current_channel_id}")
            
        except NotFoundError:
            logger.warning(f"Chat settings not available for channel {self.current_channel_id}")
        except Exception as e:
            logger.error(f"Failed to load chat settings: {e}")
    
    def save_chat_settings(self):
        """Save chat settings."""
        if not self.current_channel_id:
            self.show_error("No channel selected")
            return
        
        try:
            interactivity_manager.update_chat_settings(
                self.current_channel_id,
                enabled=self.chat_enabled_check.isChecked(),
                moderation=self.chat_moderation_combo.currentText(),
                require_login=self.chat_require_login_check.isChecked(),
                slow_mode=self.chat_slow_mode_check.isChecked(),
                slow_mode_interval=self.chat_slow_interval_spin.value()
            )
            
            self.show_success("Chat settings saved successfully")
            logger.info(f"Saved chat settings for channel {self.current_channel_id}")
            
        except Exception as e:
            self.show_error(f"Failed to save chat settings: {str(e)}")
    
    def load_polls(self):
        """Load polls for selected channel."""
        if not self.current_channel_id:
            return
        
        if not hasattr(self, 'polls_table'):
            logger.warning("Polls table UI not initialized yet")
            return
        
        try:
            polls = interactivity_manager.list_polls(self.current_channel_id)
            
            self.polls_table.setRowCount(len(polls))
            
            for row, poll in enumerate(polls):
                self.polls_table.setItem(row, 0, QTableWidgetItem(poll.get('id', '')))
                self.polls_table.setItem(row, 1, QTableWidgetItem(poll.get('question', '')))
                self.polls_table.setItem(row, 2, QTableWidgetItem(poll.get('status', '')))
                
                # Actions button
                actions_btn = QPushButton("Close")
                actions_btn.clicked.connect(lambda checked, p=poll: self.close_poll(p.get('id')))
                self.polls_table.setCellWidget(row, 3, actions_btn)
            
            logger.info(f"Loaded {len(polls)} polls for channel {self.current_channel_id}")
            
        except NotFoundError:
            logger.warning(f"Polls not available for channel {self.current_channel_id}")
            self.polls_table.setRowCount(0)
        except Exception as e:
            logger.error(f"Failed to load polls: {e}")
    
    def create_poll(self):
        """Create a new poll."""
        if not self.current_channel_id:
            self.show_error("No channel selected")
            return
        
        dialog = CreatePollDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            poll_data = dialog.get_poll_data()
            
            try:
                interactivity_manager.create_poll(
                    self.current_channel_id,
                    poll_data['question'],
                    poll_data['options'],
                    poll_data['duration']
                )
                
                self.show_success("Poll created successfully")
                self.load_polls()
                
            except Exception as e:
                self.show_error(f"Failed to create poll: {str(e)}")
    
    def close_poll(self, poll_id: str):
        """Close a poll."""
        if not self.current_channel_id:
            return
        
        try:
            interactivity_manager.close_poll(self.current_channel_id, poll_id)
            self.show_success("Poll closed")
            self.load_polls()
        except Exception as e:
            self.show_error(f"Failed to close poll: {str(e)}")
    
    def load_qa_settings(self):
        """Load Q&A settings."""
        if not self.current_channel_id:
            return
        
        if not hasattr(self, 'qa_enabled_check'):
            logger.warning("Q&A settings UI not initialized yet")
            return
        
        try:
            settings = interactivity_manager.get_qa_settings(self.current_channel_id)
            
            self.qa_enabled_check.setChecked(settings.get('enabled', False))
            self.qa_moderation_check.setChecked(settings.get('moderation', False))
            
            logger.info(f"Loaded Q&A settings for channel {self.current_channel_id}")
            
        except NotFoundError:
            logger.warning(f"Q&A settings not available for channel {self.current_channel_id}")
        except Exception as e:
            logger.error(f"Failed to load Q&A settings: {e}")
    
    def save_qa_settings(self):
        """Save Q&A settings."""
        if not self.current_channel_id:
            self.show_error("No channel selected")
            return
        
        try:
            interactivity_manager.update_qa_settings(
                self.current_channel_id,
                enabled=self.qa_enabled_check.isChecked(),
                moderation=self.qa_moderation_check.isChecked()
            )
            
            self.show_success("Q&A settings saved successfully")
            logger.info(f"Saved Q&A settings for channel {self.current_channel_id}")
            
        except Exception as e:
            self.show_error(f"Failed to save Q&A settings: {str(e)}")
    
    def refresh(self):
        """Refresh all settings."""
        self.load_settings()

# Made with Bob
