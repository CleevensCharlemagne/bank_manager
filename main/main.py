from database.database import create_database
from screens.home import EcranPrincipal, FrameMenuPrincipal
from screens.clientsScreen import ClientsFrame

def main():
    create_database()
    app = EcranPrincipal()
    app.mainloop()

if __name__ == '__main__':
    main()