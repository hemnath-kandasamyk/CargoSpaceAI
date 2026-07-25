"""
Populates a fresh database with the four roles plus one sample user per
role, a warehouse, a vehicle, and a demo shipment — enough to click through
every dashboard without manually creating data first.

Run with: python scripts/seed_data.py  (from the backend/ directory)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database.session import SessionLocal
from app.models.driver import Driver
from app.models.role import Role
from app.models.shipment import Shipment, ShipmentStatus
from app.models.tracking_history import TrackingHistory
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.warehouse import Warehouse
from app.utils.security import hash_password

ROLE_NAMES = ["customer", "driver", "warehouse_staff", "admin"]


def seed():
    db = SessionLocal()
    try:
        roles = {}
        for name in ROLE_NAMES:
            role = db.query(Role).filter_by(name=name).first()
            if not role:
                role = Role(name=name)
                db.add(role)
                db.flush()
            roles[name] = role

        def get_or_create_user(name, email, role_name):
            user = db.query(User).filter_by(email=email).first()
            if not user:
                user = User(
                    name=name,
                    email=email,
                    password_hash=hash_password("password123"),
                    role_id=roles[role_name].id,
                )
                db.add(user)
                db.flush()
            return user

        customer = get_or_create_user("Demo Customer", "customer@example.com", "customer")
        driver_user = get_or_create_user("Demo Driver", "driver@example.com", "driver")
        get_or_create_user("Demo Warehouse Staff", "warehouse@example.com", "warehouse_staff")
        get_or_create_user("Demo Admin", "admin@example.com", "admin")

        warehouse = db.query(Warehouse).filter_by(name="Chennai Hub").first()
        if not warehouse:
            warehouse = Warehouse(name="Chennai Hub", location="Chennai, TN", capacity_units=1000, current_load_units=250)
            db.add(warehouse)
            db.flush()

        vehicle = db.query(Vehicle).filter_by(plate_number="TN-01-AB-1234").first()
        if not vehicle:
            vehicle = Vehicle(plate_number="TN-01-AB-1234", type="van", capacity_kg=500)
            db.add(vehicle)
            db.flush()

        driver = db.query(Driver).filter_by(user_id=driver_user.id).first()
        if not driver:
            driver = Driver(user_id=driver_user.id, vehicle_id=vehicle.id, license_number="DL123456")
            db.add(driver)
            db.flush()

        existing_shipment = db.query(Shipment).filter_by(customer_id=customer.id).first()
        if not existing_shipment:
            shipment = Shipment(
                customer_id=customer.id,
                driver_id=driver.id,
                origin_warehouse_id=warehouse.id,
                destination_address="12 MG Road, Bengaluru",
                weight_kg=8.5,
                declared_value=2500.00,
                status=ShipmentStatus.IN_TRANSIT,
            )
            db.add(shipment)
            db.flush()
            db.add(TrackingHistory(shipment_id=shipment.id, status=ShipmentStatus.BOOKED, location="Chennai Hub"))
            db.add(TrackingHistory(shipment_id=shipment.id, status=ShipmentStatus.IN_TRANSIT, location="En route to Bengaluru"))

        db.commit()
        print("Seed data created successfully.")
        print("Login with any of: customer@example.com / driver@example.com / "
              "warehouse@example.com / admin@example.com, password: password123")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
