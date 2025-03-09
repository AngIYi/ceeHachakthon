from app import app, db, User

# Create the database and tables
with app.app_context():
    db.create_all()

#Checking
#with app.app_context():
    #users = User.query.all()
    #for user in users:
        #print(f"Username: {user.username}, Role: {user.role}")

    # Add some initial users
    user1 = User(username="user1", password="password1", role="user")
    user2 = User(username="user2", password="password2", role="user")
    agent1 = User(username="agent1", password="password1", role="agent")
    agent2 = User(username="agent2", password="password2", role="agent")

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(agent1)
    db.session.add(agent2)
    db.session.commit()