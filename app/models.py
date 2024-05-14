from app import db
from bson import ObjectId

# Define the collection
attendance_collection = db['attendance']

class Attendance:
    @staticmethod
    def record(name, id_number, timestamp):
        """
        Record attendance data in the database.
        """
        data = {'name': name, 'idNumber': id_number, 'timestamp': timestamp}
        attendance_collection.insert_one(data)

    @staticmethod
    def delete_all():
        """
        Delete all attendance records from the database.
        """
        try:
            attendance_collection.delete_many({})
            print("All attendance records deleted successfully")
        except Exception as e:
            # Log the error for debugging purposes
            print(f"Error deleting attendance records: {e}")

    @staticmethod
    def get_all():
        """
        Retrieve all attendance records from the database.
        """
        try:
            # Query all documents from the attendance collection
            all_attendance = list(attendance_collection.find())

            # Convert ObjectId to string for serialization
            for record in all_attendance:
                record['_id'] = str(record['_id'])

            return all_attendance
        except Exception as e:
            # Log the error for debugging purposes
            print(f"Error retrieving attendance records: {e}")
            return []


