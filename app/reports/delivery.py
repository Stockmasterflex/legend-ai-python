"""
Report Delivery System

Provides multiple delivery methods for reports:
- Email delivery
- Google Drive upload
- Local file save
- Share via link
- Archive in dashboard
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from io import BytesIO
from enum import Enum
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path
import logging

from pydantic import BaseModel, Field, EmailStr

logger = logging.getLogger(__name__)


class DeliveryMethod(str, Enum):
    """Available delivery methods"""
    EMAIL = "email"
    GOOGLE_DRIVE = "google_drive"
    LOCAL_FILE = "local_file"
    SHARE_LINK = "share_link"
    DASHBOARD = "dashboard"


class EmailConfig(BaseModel):
    """Email delivery configuration"""
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str
    smtp_password: str
    from_email: EmailStr
    to_emails: List[EmailStr]
    cc_emails: List[EmailStr] = Field(default_factory=list)
    bcc_emails: List[EmailStr] = Field(default_factory=list)
    subject_template: str = "Trading Report - {date}"
    body_template: str = "Please find attached your trading report for {date}."


class GoogleDriveConfig(BaseModel):
    """Google Drive delivery configuration"""
    credentials_path: str
    folder_id: Optional[str] = None  # None = root folder
    share_with_emails: List[EmailStr] = Field(default_factory=list)
    make_public: bool = False


class LocalFileConfig(BaseModel):
    """Local file save configuration"""
    save_path: str = "/tmp/reports"
    filename_template: str = "report_{date}_{type}.pdf"
    create_directories: bool = True


class ShareLinkConfig(BaseModel):
    """Share link configuration"""
    base_url: str = "https://example.com/reports"
    expiry_days: int = 7
    require_auth: bool = True


class DashboardConfig(BaseModel):
    """Dashboard archive configuration"""
    storage_path: str = "/tmp/dashboard_reports"
    max_reports: int = 100  # Maximum number of reports to keep
    auto_cleanup: bool = True


class DeliveryConfig(BaseModel):
    """Combined delivery configuration"""
    email: Optional[EmailConfig] = None
    google_drive: Optional[GoogleDriveConfig] = None
    local_file: Optional[LocalFileConfig] = None
    share_link: Optional[ShareLinkConfig] = None
    dashboard: Optional[DashboardConfig] = None


class DeliveryResult(BaseModel):
    """Result of a delivery attempt"""
    method: DeliveryMethod
    success: bool
    message: str
    delivery_url: Optional[str] = None
    delivered_at: datetime = Field(default_factory=datetime.now)


class ReportDelivery:
    """Handles report delivery via multiple methods"""

    def __init__(self):
        self.delivery_history: List[DeliveryResult] = []

    async def deliver(
        self,
        report_buffer: BytesIO,
        filename: str,
        method: DeliveryMethod,
        config: DeliveryConfig,
    ) -> bool:
        """Deliver a report via specified method"""
        try:
            if method == DeliveryMethod.EMAIL:
                return await self._deliver_email(report_buffer, filename, config.email)

            elif method == DeliveryMethod.GOOGLE_DRIVE:
                return await self._deliver_google_drive(report_buffer, filename, config.google_drive)

            elif method == DeliveryMethod.LOCAL_FILE:
                return await self._deliver_local_file(report_buffer, filename, config.local_file)

            elif method == DeliveryMethod.SHARE_LINK:
                return await self._deliver_share_link(report_buffer, filename, config.share_link)

            elif method == DeliveryMethod.DASHBOARD:
                return await self._deliver_dashboard(report_buffer, filename, config.dashboard)

            else:
                logger.error(f"Unknown delivery method: {method}")
                return False

        except Exception as e:
            logger.error(f"Error delivering report via {method}: {e}", exc_info=True)
            return False

    async def _deliver_email(
        self,
        report_buffer: BytesIO,
        filename: str,
        config: Optional[EmailConfig]
    ) -> bool:
        """Deliver report via email"""
        if not config:
            logger.error("Email configuration not provided")
            return False

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = config.from_email
            msg['To'] = ', '.join(config.to_emails)

            if config.cc_emails:
                msg['Cc'] = ', '.join(config.cc_emails)

            # Format subject and body
            date_str = datetime.now().strftime("%B %d, %Y")
            msg['Subject'] = config.subject_template.format(date=date_str)

            body = config.body_template.format(date=date_str)
            msg.attach(MIMEText(body, 'plain'))

            # Attach PDF
            report_buffer.seek(0)
            pdf_attachment = MIMEApplication(report_buffer.read(), _subtype='pdf')
            pdf_attachment.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(pdf_attachment)

            # Send email
            with smtplib.SMTP(config.smtp_host, config.smtp_port) as server:
                server.starttls()
                server.login(config.smtp_user, config.smtp_password)

                recipients = config.to_emails + config.cc_emails + config.bcc_emails
                server.send_message(msg, from_addr=config.from_email, to_addrs=recipients)

            logger.info(f"Email sent successfully to {len(recipients)} recipients")

            self.delivery_history.append(DeliveryResult(
                method=DeliveryMethod.EMAIL,
                success=True,
                message=f"Sent to {len(recipients)} recipients",
            ))

            return True

        except Exception as e:
            logger.error(f"Failed to send email: {e}", exc_info=True)

            self.delivery_history.append(DeliveryResult(
                method=DeliveryMethod.EMAIL,
                success=False,
                message=str(e),
            ))

            return False

    async def _deliver_google_drive(
        self,
        report_buffer: BytesIO,
        filename: str,
        config: Optional[GoogleDriveConfig]
    ) -> bool:
        """Deliver report to Google Drive"""
        if not config:
            logger.error("Google Drive configuration not provided")
            return False

        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaIoBaseUpload

            # Load credentials
            credentials = service_account.Credentials.from_service_account_file(
                config.credentials_path,
                scopes=['https://www.googleapis.com/auth/drive.file']
            )

            # Build Drive API client
            service = build('drive', 'v3', credentials=credentials)

            # Prepare file metadata
            file_metadata = {
                'name': filename,
            }

            if config.folder_id:
                file_metadata['parents'] = [config.folder_id]

            # Upload file
            report_buffer.seek(0)
            media = MediaIoBaseUpload(
                report_buffer,
                mimetype='application/pdf',
                resumable=True
            )

            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()

            file_id = file.get('id')
            web_link = file.get('webViewLink')

            # Share with specified emails
            for email in config.share_with_emails:
                permission = {
                    'type': 'user',
                    'role': 'reader',
                    'emailAddress': email,
                }
                service.permissions().create(
                    fileId=file_id,
                    body=permission,
                    sendNotificationEmail=True
                ).execute()

            # Make public if requested
            if config.make_public:
                permission = {
                    'type': 'anyone',
                    'role': 'reader',
                }
                service.permissions().create(
                    fileId=file_id,
                    body=permission
                ).execute()

            logger.info(f"Uploaded to Google Drive: {web_link}")

            self.delivery_history.append(DeliveryResult(
                method=DeliveryMethod.GOOGLE_DRIVE,
                success=True,
                message=f"Uploaded successfully",
                delivery_url=web_link,
            ))

            return True

        except Exception as e:
            logger.error(f"Failed to upload to Google Drive: {e}", exc_info=True)

            self.delivery_history.append(DeliveryResult(
                method=DeliveryMethod.GOOGLE_DRIVE,
                success=False,
                message=str(e),
            ))

            return False

    async def _deliver_local_file(
        self,
        report_buffer: BytesIO,
        filename: str,
        config: Optional[LocalFileConfig]
    ) -> bool:
        """Save report to local file system"""
        if not config:
            logger.error("Local file configuration not provided")
            return False

        try:
            # Create directory if needed
            save_dir = Path(config.save_path)
            if config.create_directories:
                save_dir.mkdir(parents=True, exist_ok=True)

            # Generate filename
            date_str = datetime.now().strftime("%Y%m%d")
            report_type = filename.split('_')[0] if '_' in filename else 'report'

            final_filename = config.filename_template.format(
                date=date_str,
                type=report_type,
            )

            # Save file
            file_path = save_dir / final_filename
            report_buffer.seek(0)
            with open(file_path, 'wb') as f:
                f.write(report_buffer.read())

            logger.info(f"Saved report to: {file_path}")

            self.delivery_history.append(DeliveryResult(
                method=DeliveryMethod.LOCAL_FILE,
                success=True,
                message=f"Saved to {file_path}",
                delivery_url=str(file_path),
            ))

            return True

        except Exception as e:
            logger.error(f"Failed to save local file: {e}", exc_info=True)

            self.delivery_history.append(DeliveryResult(
                method=DeliveryMethod.LOCAL_FILE,
                success=False,
                message=str(e),
            ))

            return False

    async def _deliver_share_link(
        self,
        report_buffer: BytesIO,
        filename: str,
        config: Optional[ShareLinkConfig]
    ) -> bool:
        """Generate shareable link for report"""
        if not config:
            logger.error("Share link configuration not provided")
            return False

        try:
            # First save the file locally
            import hashlib
            import uuid

            # Generate unique ID
            report_id = str(uuid.uuid4())[:8]

            # Save to temp location
            temp_dir = Path("/tmp/shared_reports")
            temp_dir.mkdir(parents=True, exist_ok=True)

            file_path = temp_dir / f"{report_id}_{filename}"
            report_buffer.seek(0)
            with open(file_path, 'wb') as f:
                f.write(report_buffer.read())

            # Generate share link
            share_url = f"{config.base_url}/{report_id}/{filename}"

            # Store metadata (in production, this would go to a database)
            metadata = {
                'report_id': report_id,
                'filename': filename,
                'file_path': str(file_path),
                'share_url': share_url,
                'created_at': datetime.now(),
                'expires_at': datetime.now() + timedelta(days=config.expiry_days),
                'require_auth': config.require_auth,
            }

            logger.info(f"Created share link: {share_url}")

            self.delivery_history.append(DeliveryResult(
                method=DeliveryMethod.SHARE_LINK,
                success=True,
                message=f"Share link created (expires in {config.expiry_days} days)",
                delivery_url=share_url,
            ))

            return True

        except Exception as e:
            logger.error(f"Failed to create share link: {e}", exc_info=True)

            self.delivery_history.append(DeliveryResult(
                method=DeliveryMethod.SHARE_LINK,
                success=False,
                message=str(e),
            ))

            return False

    async def _deliver_dashboard(
        self,
        report_buffer: BytesIO,
        filename: str,
        config: Optional[DashboardConfig]
    ) -> bool:
        """Archive report in dashboard"""
        if not config:
            logger.error("Dashboard configuration not provided")
            return False

        try:
            # Create storage directory
            storage_dir = Path(config.storage_path)
            storage_dir.mkdir(parents=True, exist_ok=True)

            # Save report
            file_path = storage_dir / filename
            report_buffer.seek(0)
            with open(file_path, 'wb') as f:
                f.write(report_buffer.read())

            # Cleanup old reports if needed
            if config.auto_cleanup:
                self._cleanup_dashboard(storage_dir, config.max_reports)

            logger.info(f"Archived in dashboard: {file_path}")

            self.delivery_history.append(DeliveryResult(
                method=DeliveryMethod.DASHBOARD,
                success=True,
                message=f"Archived in dashboard",
                delivery_url=str(file_path),
            ))

            return True

        except Exception as e:
            logger.error(f"Failed to archive in dashboard: {e}", exc_info=True)

            self.delivery_history.append(DeliveryResult(
                method=DeliveryMethod.DASHBOARD,
                success=False,
                message=str(e),
            ))

            return False

    def _cleanup_dashboard(self, storage_dir: Path, max_reports: int):
        """Clean up old reports from dashboard"""
        # Get all PDF files sorted by modification time
        reports = sorted(
            storage_dir.glob("*.pdf"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        # Delete oldest reports if exceeding max
        if len(reports) > max_reports:
            for report in reports[max_reports:]:
                report.unlink()
                logger.info(f"Deleted old report: {report.name}")

    def get_delivery_history(
        self,
        method: Optional[DeliveryMethod] = None,
        limit: int = 100
    ) -> List[DeliveryResult]:
        """Get delivery history"""
        history = self.delivery_history

        if method:
            history = [h for h in history if h.method == method]

        return history[-limit:]
