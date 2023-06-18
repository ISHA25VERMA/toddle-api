import graphene 
from .models import User
from sqlalchemy.exc import IntegrityError
from config.db import db_session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_graphql_auth import create_access_token, create_refresh_token, mutation_jwt_refresh_token_required, get_jwt_identity, query_header_jwt_required
from .serializer import UserType

class Register(graphene.Mutation):
    class Arguments:
        username = graphene.String(required = True)
        password = graphene.String(required = True)
        role = graphene.String(required = True)
    
    message = graphene.String()
    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @query_header_jwt_required
    def mutate(cls, _,info, username, password, role):
        user_id = get_jwt_identity()
        if(User.query.filter_by(id=user_id).first().role != 'admin'):
            return Register(error = "You are not authorized to create a user")
        try:
            if(role not in ['admin', 'teacher', 'student']):
                return Register(error = "Role must be admin, teacher or student")
            new_user = User(
                username=username, 
                password=generate_password_hash(password, method="sha256"), 
                role = role)
            
            db_session.add(new_user)
            db_session.commit()
        except IntegrityError as e:
             return Register(error = f'{e.origin}')
        
        return Register(success = True, message = f'User {username} added successfully')
    

    
class Authentication(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    access_token = graphene.String()
    refresh_token = graphene.String()
    error = graphene.String()

    @classmethod
    def mutate(cls, _, info, username, password):
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return Authentication(error="Invalid username or password")
        return Authentication(access_token= create_access_token(user.id), refresh_token= create_refresh_token(user.id))


class RefreshMutation(graphene.Mutation):
    class Aruguemnts:
        refresh_token = graphene.String(required=True)
    
    new_token = graphene.String()

    @classmethod
    @mutation_jwt_refresh_token_required
    def mutate(cls, _):
        current_user = get_jwt_identity()
        return RefreshMutation(new_token = create_access_token(identity=current_user))
    

class Mutation(graphene.ObjectType):
    register = Register.Field()
    authenticate = Authentication.Field()
    refresh = RefreshMutation.Field()

class Query(graphene.ObjectType):
    me = graphene.Field(UserType)

    users = graphene.List(UserType)

    @classmethod
    @query_header_jwt_required
    def resolve_me(cls, info, *args):
        user_id = get_jwt_identity()
        return User.query.filter_by(id=user_id).first()
    
    @classmethod
    @query_header_jwt_required
    def resolve_users(cls, info, *args):
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if(user.role == 'admin'):
            return User.query.all()
        else:
            return User.query.filter_by(id=user_id).all()