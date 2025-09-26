from datetime import datetime
from database.db import Sessionlocal
from utils.otp.otp_model import OTP

def cleanup_otps():
    db = Sessionlocal()
    now = datetime.utcnow()
    expired = db.query(OTP).filter(OTP.expires_at < now).all()

    for record in expired:
        db.delete(record)
        print(f"[Cleanup] Removed expired OTP for {record.username}")

    db.commit()
    db.close()

if __name__ == "__main__":
    cleanup_otps()