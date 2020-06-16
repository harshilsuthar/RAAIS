from project import db


class DatasetVO(db.Model):
    __tablename__ = 'datasetmaster'
    datasetId = db.Column('datasetId', db.Integer, primary_key=True, autoincrement=True)
    datasetFilename = db.Column('datasetFilename', db.String(100))
    uploadDate = db.Column('uploadDate', db.Date)
    uploadTime = db.Column('uploadTime', db.Time)
    datasetFilePath = db.Column('datasetFilePath', db.String(1000))

    def as_dict(self):
        return {
            'datasetId': self.datasetId,
            'datasetFilename': self.datasetFilename,
            'uploadDate': self.uploadDate,
            'uploadTime': self.uploadTime,
            'datasetFilePath': self.datasetFilePath
        }


db.create_all()
