import os
import peewee as pw
import datetime
from playhouse.postgres_ext import PostgresqlExtDatabase

db = PostgresqlExtDatabase(os.getenv('DATABASE'))


class BaseModel(pw.Model):
    created_at = pw.DateTimeField(default=datetime.datetime.now)
    updated_at = pw.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.errors = []
        self.validate()

        if len(self.errors) == 0:
            self.updated_at = datetime.datetime.now()
            return super(BaseModel, self).save(*args, **kwargs)
        else:
            return 0

    class Meta:
        database = db
        legacy_table_names = False


class Store(BaseModel):
    name = pw.CharField(unique=True)

    def validate(self):
        duplicate_stores = Store.get_or_none(Store.name == self.name)

        if duplicate_stores:
            self.errors.append('Store name not unique')


class Warehouse(BaseModel):
    # unique true makes it so that only 1 warehouse can use a particular store. so now 1 store can only have 1 warehouse. removing unique turns it into 1 store can have many warehouses .i.e. any number of warehouses can share the same store
    store = pw.ForeignKeyField(Store, backref='warehouses', unique=True)
    location = pw.TextField()


class Product(BaseModel):
    name = pw.CharField(index=True)
    description = pw.TextField()
    warehouse = pw.ForeignKeyField(Warehouse, backref='products')
    color = pw.CharField(null=True)
