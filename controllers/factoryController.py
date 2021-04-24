from database import User, UserSchema, Room, RoomSchema, Hostel, HostelSchema, Trait, TraitSchema, db


models = {
    'user' : [User, UserSchema],
    'room' : [Room, RoomSchema],
    'trait' : [Trait, TraitSchema],
    'hostel' : [Hostel, HostelSchema]
}


def get_all(model):
    Model = models[model][0]
    ModelSchema = models[model][1]
    data = Model.query.all()
    data = ModelSchema(many=True).dump(data)
    return data

def create_one(model, args):
    Model = models[model][0]
    ModelSchema = models[model][1]
    data = ModelSchema().load(args)
    data = data.create()
    return  ModelSchema().dump(data)

def get_one(model, id, format='json'):
    Model = models[model][0]
    ModelSchema = models[model][1]
    data = Model.query.get_or_404(id)
    if format == 'obj':
        return data
    else:
        data = ModelSchema().dump(data)
        return data

def delete_one(model, id):
    Model = models[model][0]
    ModelSchema = models[model][1]
    data = Model.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    return '', 204

# def update_one(model, id, args):
#     Model = models[model][0]
#     ModelSchema = models[model][1]
#     Model.query.get_or_404(id)

#     #Loop through the keys in patc






