"""
PyQt5 GUI for Secure Message Chat System - PROFESSIONAL DESIGN v2.0
Ultra-modern, beautiful interface with full branding
"""

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QLabel, 
                             QListWidget, QListWidgetItem, QTextEdit, QDialog,
                             QMessageBox, QComboBox, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon, QColor, QLinearGradient, QPalette, QPixmap, QPainter
import sys


class StyledLineEdit(QLineEdit):
    """Modern, elegant line edit with icons"""
    def __init__(self, placeholder="", icon_emoji=""):
        super().__init__()
        self.setPlaceholderText(f"  {icon_emoji} {placeholder}")
        self.setMinimumHeight(50)
        self.setFont(QFont('Segoe UI', 11))
        self.setStyleSheet("""
            QLineEdit {
                padding: 12px 15px;
                border: 2px solid #E8E8E8;
                border-radius: 10px;
                background-color: #FFFFFF;
                color: #333333;
                selection-background-color: #1E88E5;
            }
            QLineEdit:focus {
                border: 2px solid #1E88E5;
                background-color: #FFFFFF;
                box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.1);
            }
            QLineEdit::placeholder {
                color: #BDBDBD;
            }
        """)


class StyledButton(QPushButton):
    """Modern, beautiful button with gradient"""
    def __init__(self, text, color="#1E88E5", icon=""):
        super().__init__(f"{icon} {text}")
        self.setMinimumHeight(50)
        self.setFont(QFont('Segoe UI', 12, QFont.Bold))
        
        color_map = {
            "#1E88E5": ("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1E88E5, stop:1 #1565C0);", 
                       "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2196F3, stop:1 #1976D2);"),
            "#43A047": ("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #43A047, stop:1 #2E7D32);",
                       "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4CAF50, stop:1 #388E3C);"),
            "#E53935": ("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #E53935, stop:1 #C62828);",
                       "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F44336, stop:1 #D32F2F);"),
        }
        
        normal, hover = color_map.get(color, (f"background-color: {color};", f"background-color: {color};"))
        
        self.setStyleSheet(f"""
            QPushButton {{
                {normal}
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                padding: 10px 20px;
                text-align: center;
            }}
            QPushButton:hover {{
                {hover}
            }}
            QPushButton:pressed {{
                padding: 12px 18px;
            }}
        """)


class LoginWindow(QDialog):
    """Beautiful, Modern Login & Registration Interface"""
    def __init__(self, chat_system):
        super().__init__()
        self.chat_system = chat_system
        self.current_user = None
        self.is_login_mode = True
        self.initUI()
    
    def initUI(self):
        """Create beautiful interface"""
        self.setWindowTitle('🔐 Secure Message Chat System')
        self.setGeometry(300, 100, 700, 750)
        self.setStyleSheet("background-color: #F8F9FA;")
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ========== HEADER WITH GRADIENT ==========
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1E88E5, stop:0.5 #1565C0, stop:1 #0D47A1);
                border-radius: 20px 20px 0 0;
            }
        """)
        header.setMinimumHeight(220)
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 40, 0, 40)
        header_layout.setSpacing(10)
        
        # Lock Icon / Logo
        logo = QLabel('🔐')
        logo.setFont(QFont('Arial', 60))
        logo.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(logo)
        
        # Project Title
        title = QLabel('Secure Message Chat System')
        title_font = QFont('Segoe UI', 26, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; letter-spacing: 1px;")
        header_layout.addWidget(title)
        
        # Tagline
        tagline = QLabel('🛡️ End-to-End Encrypted • Secure Communication • Privacy First')
        tagline_font = QFont('Segoe UI', 10)
        tagline.setFont(tagline_font)
        tagline.setAlignment(Qt.AlignCenter)
        tagline.setStyleSheet("color: #B3E5FC; font-style: italic;")
        header_layout.addWidget(tagline)
        
        header.setLayout(header_layout)
        main_layout.addWidget(header)
        
        # ========== CONTENT AREA ==========
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(50, 50, 50, 50)
        content_layout.setSpacing(20)
        
        # Mode Title
        self.mode_title = QLabel('Login to Your Account')
        mode_font = QFont('Segoe UI', 18, QFont.Bold)
        self.mode_title.setFont(mode_font)
        self.mode_title.setStyleSheet("color: #212121; margin-bottom: 10px;")
        content_layout.addWidget(self.mode_title)
        
        # Description
        self.description = QLabel('Enter your credentials to access your secure messages')
        desc_font = QFont('Segoe UI', 11)
        self.description.setFont(desc_font)
        self.description.setStyleSheet("color: #666666;")
        content_layout.addWidget(self.description)
        
        content_layout.addSpacing(10)
        
        # Username Field
        username_label = QLabel('👤 Username')
        username_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
        username_label.setStyleSheet("color: #333333;")
        content_layout.addWidget(username_label)
        
        self.username_input = StyledLineEdit("Enter your username", "")
        content_layout.addWidget(self.username_input)
        
        # Password Field
        password_label = QLabel('🔑 Password')
        password_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
        password_label.setStyleSheet("color: #333333;")
        content_layout.addWidget(password_label)
        
        self.password_input = StyledLineEdit("Enter your password", "")
        self.password_input.setEchoMode(QLineEdit.Password)
        content_layout.addWidget(self.password_input)
        
        content_layout.addSpacing(15)
        
        # Primary Action Button
        self.primary_btn = StyledButton('LOGIN', '#1E88E5', '📱')
        self.primary_btn.clicked.connect(self.login)
        content_layout.addWidget(self.primary_btn)
        
        # Secondary Action Button
        self.secondary_btn = StyledButton('REGISTER', '#43A047', '✨')
        self.secondary_btn.clicked.connect(self.switch_to_register)
        content_layout.addWidget(self.secondary_btn)
        
        # Toggle Link
        toggle_text = QLabel("Don't have an account? <a href='#' style='color: #1E88E5;'>Click here to register</a>")
        toggle_text.setFont(QFont('Segoe UI', 10))
        toggle_text.setAlignment(Qt.AlignCenter)
        toggle_text.setStyleSheet("color: #666666;")
        self.toggle_label = toggle_text
        self.toggle_label.linkActivated.connect(self.switch_to_register)
        content_layout.addWidget(self.toggle_label)
        
        # Status Message
        self.status_label = QLabel('')
        status_font = QFont('Segoe UI', 11, QFont.Bold)
        self.status_label.setFont(status_font)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("padding: 10px; border-radius: 5px;")
        content_layout.addWidget(self.status_label)
        
        content_layout.addStretch()
        
        # Features info at bottom
        features = QLabel('✓ Military-grade encryption  ✓ Zero-knowledge architecture  ✓ Instant delivery')
        features_font = QFont('Segoe UI', 9)
        features.setFont(features_font)
        features.setAlignment(Qt.AlignCenter)
        features.setStyleSheet("color: #999999; font-style: italic;")
        content_layout.addWidget(features)
        
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)
    
    def login(self):
        """Handle login"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self.show_error('Please enter both username and password')
            return
        
        user = self.chat_system.login_user(username, password)
        if user:
            self.current_user = user
            self.show_success('✓ Login successful! Welcome back!')
            QTimer.singleShot(1000, self.accept)
        else:
            self.show_error('❌ Invalid username or password')
    
    def register(self):
        """Handle registration"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self.show_error('Please enter both username and password')
            return
        
        if len(password) < 3:
            self.show_error('Password must be at least 3 characters')
            return
        
        if self.chat_system.register_user(username, password):
            self.show_success('✓ Registration successful! Now login with your credentials.')
            self.username_input.clear()
            self.password_input.clear()
            QTimer.singleShot(2000, self.switch_to_login)
        else:
            self.show_error('❌ Username already exists')
    
    def switch_to_register(self):
        """Switch to registration mode"""
        if self.is_login_mode:
            self.is_login_mode = False
            self.mode_title.setText('Create New Account')
            self.description.setText('Join our secure messaging community today')
            self.primary_btn.setText('✨ REGISTER')
            self.primary_btn.clicked.disconnect()
            self.primary_btn.clicked.connect(self.register)
            self.secondary_btn.setText('📱 LOGIN')
            self.toggle_label.setText("Already have an account? <a href='#' style='color: #1E88E5;'>Click here to login</a>")
            self.status_label.setText('')
            self.username_input.clear()
            self.password_input.clear()
    
    def switch_to_login(self):
        """Switch to login mode"""
        if not self.is_login_mode:
            self.is_login_mode = True
            self.mode_title.setText('Login to Your Account')
            self.description.setText('Enter your credentials to access your secure messages')
            self.primary_btn.setText('📱 LOGIN')
            self.primary_btn.clicked.disconnect()
            self.primary_btn.clicked.connect(self.login)
            self.secondary_btn.setText('✨ REGISTER')
            self.toggle_label.setText("Don't have an account? <a href='#' style='color: #1E88E5;'>Click here to register</a>")
            self.status_label.setText('')
            self.username_input.clear()
            self.password_input.clear()
    
    def show_error(self, message):
        """Show error with nice styling"""
        self.status_label.setText(message)
        self.status_label.setStyleSheet("""
            background-color: #FFEBEE;
            color: #C62828;
            padding: 12px;
            border-radius: 8px;
            border-left: 4px solid #C62828;
        """)
    
    def show_success(self, message):
        """Show success with nice styling"""
        self.status_label.setText(message)
        self.status_label.setStyleSheet("""
            background-color: #E8F5E9;
            color: #2E7D32;
            padding: 12px;
            border-radius: 8px;
            border-left: 4px solid #2E7D32;
        """)


class ChatWindow(QMainWindow):
    """Modern, Professional Chat Interface"""
    def __init__(self, chat_system, user):
        super().__init__()
        self.chat_system = chat_system
        self.current_user = user
        self.selected_recipient = None
        self.initUI()
    
    def initUI(self):
        """Initialize beautiful chat window"""
        self.setWindowTitle(f'🔐 Secure Chat - {self.current_user.get_username()}')
        self.setGeometry(100, 100, 1100, 750)
        self.setStyleSheet("background-color: #FAFAFA;")
        
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ========== LEFT SIDEBAR ==========
        sidebar = QFrame()
        sidebar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1E3A8A, stop:1 #1E88E5);
                border-right: 2px solid #1565C0;
            }
        """)
        sidebar.setMaximumWidth(300)
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(25, 25, 25, 25)
        sidebar_layout.setSpacing(20)
        
        # Current User Profile
        user_frame = QFrame()
        user_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        user_layout = QVBoxLayout()
        user_layout.setContentsMargins(0, 0, 0, 0)
        user_layout.setSpacing(5)
        
        user_avatar = QLabel('👤')
        user_avatar.setFont(QFont('Arial', 32))
        user_avatar.setAlignment(Qt.AlignCenter)
        user_layout.addWidget(user_avatar)
        
        username_display = QLabel(self.current_user.get_username().upper())
        username_font = QFont('Segoe UI', 13, QFont.Bold)
        username_display.setFont(username_font)
        username_display.setAlignment(Qt.AlignCenter)
        username_display.setStyleSheet("color: white;")
        user_layout.addWidget(username_display)
        
        status = QLabel('🟢 Online & Encrypted')
        status_font = QFont('Segoe UI', 9)
        status.setFont(status_font)
        status.setAlignment(Qt.AlignCenter)
        status.setStyleSheet("color: #B3E5FC;")
        user_layout.addWidget(status)
        
        user_frame.setLayout(user_layout)
        sidebar_layout.addWidget(user_frame)
        
        # Users List Title
        online_title = QLabel('💬 ONLINE CONTACTS')
        online_title.setFont(QFont('Segoe UI', 11, QFont.Bold))
        online_title.setStyleSheet("color: #E3F2FD;")
        sidebar_layout.addWidget(online_title)
        
        # Users List
        self.user_list = QListWidget()
        self.user_list.setStyleSheet("""
            QListWidget {
                background-color: rgba(255, 255, 255, 0.05);
                border: none;
                border-radius: 8px;
            }
            QListWidget::item {
                padding: 12px;
                color: white;
                border-radius: 6px;
                margin: 3px 0;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #43A047, stop:1 #2E7D32);
            }
            QListWidget::item:hover {
                background-color: rgba(255, 255, 255, 0.15);
            }
        """)
        self.user_list.itemClicked.connect(self.on_user_selected)
        sidebar_layout.addWidget(self.user_list)
        
        # Buttons
        refresh_btn = StyledButton('↻ Refresh', '#43A047', '🔄')
        refresh_btn.clicked.connect(self.load_users)
        sidebar_layout.addWidget(refresh_btn)
        
        logout_btn = StyledButton('Logout', '#E53935', '🚪')
        logout_btn.clicked.connect(self.logout)
        sidebar_layout.addWidget(logout_btn)
        
        sidebar_layout.addStretch()
        
        # Security Info
        security_info = QLabel('🛡️ End-to-End Encrypted\n✓ All messages encrypted')
        security_info.setFont(QFont('Segoe UI', 9))
        security_info.setAlignment(Qt.AlignCenter)
        security_info.setStyleSheet("color: #B3E5FC;")
        sidebar_layout.addWidget(security_info)
        
        sidebar.setLayout(sidebar_layout)
        main_layout.addWidget(sidebar)
        
        # ========== RIGHT CONTENT AREA ==========
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(30, 25, 30, 25)
        content_layout.setSpacing(15)
        
        # Chat Header
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                border: 1px solid #E0E0E0;
            }
        """)
        header_layout = QHBoxLayout()
        
        self.chat_title = QLabel('💬 Select a contact to start messaging')
        self.chat_title.setFont(QFont('Segoe UI', 14, QFont.Bold))
        self.chat_title.setStyleSheet("color: #1E88E5;")
        header_layout.addWidget(self.chat_title)
        header_layout.addStretch()
        header_layout.addWidget(QLabel('🔐 Encrypted'))
        
        header_frame.setLayout(header_layout)
        content_layout.addWidget(header_frame)
        
        # Messages Display
        self.message_display = QTextEdit()
        self.message_display.setReadOnly(True)
        self.message_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
                padding: 20px;
                font-family: 'Segoe UI';
                font-size: 11px;
                color: #333333;
            }
        """)
        content_layout.addWidget(self.message_display)
        
        # Message Input Section
        input_section = QFrame()
        input_section.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #E0E0E0;
                padding: 20px;
            }
        """)
        input_layout = QVBoxLayout()
        input_layout.setSpacing(12)
        
        recipient_label = QLabel('📤 Send to:')
        recipient_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
        recipient_label.setStyleSheet("color: #333333;")
        input_layout.addWidget(recipient_label)
        
        self.recipient_combo = QComboBox()
        self.recipient_combo.setMinimumHeight(40)
        self.recipient_combo.setFont(QFont('Segoe UI', 11))
        self.recipient_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                background-color: #FFFFFF;
            }
            QComboBox:focus {
                border: 2px solid #1E88E5;
            }
        """)
        self.recipient_combo.currentIndexChanged.connect(self.on_recipient_changed)
        input_layout.addWidget(self.recipient_combo)
        
        message_label = QLabel('💌 Message:')
        message_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
        message_label.setStyleSheet("color: #333333;")
        input_layout.addWidget(message_label)
        
        self.message_input = StyledLineEdit("Type your message here and press Enter to send")
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)
        
        input_section.setLayout(input_layout)
        content_layout.addWidget(input_section)
        
        # Send Button
        send_btn = StyledButton('📤 SEND SECURELY', '#43A047', '')
        send_btn.setMinimumHeight(45)
        send_btn.clicked.connect(self.send_message)
        content_layout.addWidget(send_btn)
        
        # Content widget
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget, 1)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        self.load_users()
    
    def load_users(self):
        """Load all online users"""
        self.user_list.clear()
        self.recipient_combo.clear()
        
        all_users = self.chat_system.get_all_users()
        current_username = self.current_user.get_username()
        
        count = 0
        for user in all_users:
            username = user.get_username()
            if username != current_username:
                self.user_list.addItem(f"💬 {username}")
                self.recipient_combo.addItem(username)
                count += 1
        
        if count == 0:
            self.chat_title.setText('⏳ Waiting for other users to join...')
        else:
            self.chat_title.setText(f'✓ {count} user(s) online')
    
    def on_user_selected(self, item):
        """Handle user selection"""
        username = item.text().replace("💬 ", "").strip()
        self.selected_recipient = username
        self.recipient_combo.setCurrentText(username)
        self.load_conversation()
    
    def on_recipient_changed(self):
        """Handle recipient change"""
        self.selected_recipient = self.recipient_combo.currentText()
        if self.selected_recipient:
            self.chat_title.setText(f'💬 Chat with {self.selected_recipient} 🔐')
            self.load_conversation()
    
    def load_conversation(self):
        """Load and display conversation"""
        if not self.selected_recipient:
            self.message_display.clear()
            return
        
        messages = self.chat_system.get_conversation(
            self.current_user.get_username(),
            self.selected_recipient
        )
        
        self.message_display.clear()
        
        if not messages:
            self.message_display.setText("💬 No messages yet\n\n" +
                                        "Start the conversation by typing a message below!\n\n" +
                                        "🔐 All messages are end-to-end encrypted\n" +
                                        "✓ Only you and the recipient can read them")
            return
        
        html_content = "<div style='font-family: Segoe UI;'>"
        for msg in messages:
            sender = msg['sender']
            timestamp = msg['timestamp']
            
            try:
                decrypted = self.chat_system.decrypt_message(msg['content_encrypted'])
            except:
                decrypted = "[Unable to decrypt]"
            
            if sender == self.current_user.get_username():
                html_content += f"""
                <div style='margin: 10px 0; padding: 10px; background-color: #E3F2FD; 
                           border-radius: 8px; text-align: right;'>
                    <div style='font-size: 9px; color: #666;'>📤 You • {timestamp}</div>
                    <div style='margin-top: 5px; color: #333;'>{decrypted}</div>
                </div>
                """
            else:
                html_content += f"""
                <div style='margin: 10px 0; padding: 10px; background-color: #F5F5F5; 
                           border-radius: 8px;'>
                    <div style='font-size: 9px; color: #666;'>📥 {sender} • {timestamp}</div>
                    <div style='margin-top: 5px; color: #333;'>{decrypted}</div>
                </div>
                """
        
        html_content += "</div>"
        self.message_display.setHtml(html_content)
        
        self.message_display.verticalScrollBar().setValue(
            self.message_display.verticalScrollBar().maximum()
        )
    
    def send_message(self):
        """Send message securely"""
        if not self.selected_recipient:
            QMessageBox.warning(self, '⚠️ Error', '❌ Please select a recipient first')
            return
        
        content = self.message_input.text().strip()
        if not content:
            QMessageBox.warning(self, '⚠️ Error', '❌ Please enter a message')
            return
        
        if self.chat_system.send_message(
            self.current_user.get_username(),
            self.selected_recipient,
            content
        ):
            self.message_input.clear()
            self.load_conversation()
            QMessageBox.information(self, '✓ Success', '✓ Message sent securely! 🔐')
        else:
            QMessageBox.critical(self, '❌ Error', '❌ Failed to send message')
    
    def logout(self):
        """Logout user"""
        reply = QMessageBox.question(self, '🚪 Logout', 
                                    'Are you sure you want to logout?',
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()


def main():
    """Main entry point"""
    from chat_system import ChatSystem
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    chat_system = ChatSystem()
    
    login_window = LoginWindow(chat_system)
    if login_window.exec_() == QDialog.Accepted:
        chat_window = ChatWindow(chat_system, login_window.current_user)
        chat_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()


if __name__ == '__main__':
    main()
