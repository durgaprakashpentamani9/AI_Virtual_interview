from sqlalchemy import select
class Repository:
    def __init__(self, db): self.db=db
    def get_all(self, model, filters=None, order_by=None):
        q=select(model)
        for k,v in (filters or {}).items(): q=q.where(getattr(model,k)==v)
        if order_by is not None: q=q.order_by(order_by)
        return list(self.db.scalars(q))
    def get_by_id(self, model, id): return self.db.get(model,id)
    def get_one(self, model, filters): return next(iter(self.get_all(model,filters)),None)
    def create(self, model, data):
        item=model(**data); self.db.add(item); self.db.commit(); self.db.refresh(item); return item
    def update_by_id(self, model, id, updates):
        item=self.get_by_id(model,id)
        if item:
            for k,v in updates.items(): setattr(item,k,v)
            self.db.commit(); self.db.refresh(item)
        return item
    def delete_by_id(self, model, id):
        item=self.get_by_id(model,id)
        if item: self.db.delete(item); self.db.commit()
        return item is not None
