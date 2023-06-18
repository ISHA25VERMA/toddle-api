from flask import Flask
from flask_graphql_auth import GraphQLAuth
from flask_graphql import GraphQLView
from .db import db_session
from .schema import schema
from graphene_file_upload.flask import FileUploadGraphQLView 

JWT_SECRET_KEY= "766521!@@$#$0479273823"

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 3600*24*30
app.config['JWT_SECRET_KEY'] = 'Bearer'



auth = GraphQLAuth(app)
app.add_url_rule('/graphql',view_func = FileUploadGraphQLView.as_view('graphql', schema=schema, graphiql=True))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


