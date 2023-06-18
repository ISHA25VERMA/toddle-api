import graphene 
from .models import Journal, Tags
from auth.models import User
from .serializer import JournalType
from sqlalchemy.exc import IntegrityError
from graphene_sqlalchemy import SQLAlchemyConnectionField
from config.db import db_session
from flask_graphql_auth import get_jwt_identity, query_header_jwt_required
from .serializer import JournalType, TagsType
from datetime import datetime
import os
from graphene_file_upload.scalars import Upload
from config.helper import file_path
from werkzeug.utils import secure_filename

class CreateJournal(graphene.Mutation):
    class Arguments:
        title = graphene.String(required = True)
        description = graphene.String(required = True)
        publish_time = graphene.DateTime(required = True)
        tags = graphene.List(graphene.Int, required = True)
        file = Upload()

    message = graphene.String()
    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @query_header_jwt_required
    def mutate(cls, _,info, title, description, publish_time, tags, file=None):
        user_id = get_jwt_identity()
        if(User.query.filter_by(id=user_id).first().role != 'teacher'):
            return CreateJournal(error = "You are not authorized to create a journal")
        try:
            if(file):
                filename = secure_filename(file.filename)
                file.save(os.path.join(file_path, filename))

            new_journal = Journal(
                title=title, 
                description=description, 
                publish_time = publish_time,
                teacher_id = User.query.filter_by(id=user_id).first().id,  
                file_path = filename if file else None
            )
            
            db_session.add(new_journal)
            db_session.commit()
        except IntegrityError as e:
            return CreateJournal(error = f'{e.origin}')
        
        try:
            for tag in tags:
                new_tag = Tags(
                    journal_id = new_journal.id,
                    student_id = tag
                )
                db_session.add(new_tag)
                db_session.commit()
        except IntegrityError as e:
            return CreateJournal(error = f'{e.origin}')
        

        return CreateJournal(success = True, message = f'Journal {title} added successfully')

class UpdateJournal(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required = True)
        title = graphene.String()
        description = graphene.String()
        publish_time = graphene.DateTime()
        tags = graphene.List(graphene.Int)

    message = graphene.String()
    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @query_header_jwt_required
    def mutate(cls, _,info, id, title= None, description= None, publish_time = None, tags = None):
        user_id = get_jwt_identity()
        
        if(Journal.query.filter_by(id=id).first().teacher_id != User.query.filter_by(id=user_id).first().id):
            return UpdateJournal(error = "You are not authorized to update a journal")
        try:
            print("creating journal object")
            journal = Journal.query.filter_by(id=id).first()
            print("journal object created")
            if(title):
                journal.title = title
                db_session.commit()
            if(description):
                print("updating description")
                journal.description = description
                db_session.commit()
            if(tags):
                for tag in Tags.query.all():
                    if(tag.journal_id == id):
                        db_session.delete(tag)
                        db_session.commit()

                for tag in tags:
                    new_tag = Tags(
                        journal_id = id,
                        student_id = tag
                    )
                    db_session.add(new_tag)
                    db_session.commit()
            if(publish_time):
                journal.publish_time = publish_time
        except IntegrityError as e:
            return UpdateJournal(error = f'{e.origin}')
        

        return UpdateJournal(success = True, message = f'Journal {journal.title} updated successfully')

class DeleteJournal(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required = True)
    
    message = graphene.String()
    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @query_header_jwt_required
    def mutate(cls, _,info, id):
        user_id = get_jwt_identity()
        if(Journal.query.filter_by(id=id).first().teacher_id != User.query.filter_by(id=user_id).first().id):
            return DeleteJournal(error = "You are not authorized to delete a journal")
        try:
            journal = Journal.query.filter_by(id=id).first()
            db_session.delete(journal)
            db_session.commit()
        except IntegrityError as e:
            return DeleteJournal(error = f'{e.origin}')
        
        return DeleteJournal(success = True, message = f'Journal {Journal.query.filter_by(id = id).title} deleted successfully')

class Mutation(graphene.ObjectType):
    create_journal = CreateJournal.Field()
    update_journal = UpdateJournal.Field()
    delete_journal = DeleteJournal.Field()

class Query(graphene.ObjectType):
    journals = graphene.List(JournalType)
    
    @classmethod
    @query_header_jwt_required
    def resolve_journals(cls, _, info,*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        
        if(user.role == 'teacher'):
            return Journal.query.filter_by(teacher_id=user.id).all()
        else:
            current_time = datetime.now()
            JournalId = [tag.journal_id for tag in Tags.query.all() if tag.student_id == user.id]
            return Journal.query.filter(Journal.id.in_(JournalId)).filter(Journal.publish_time <= current_time).all()


