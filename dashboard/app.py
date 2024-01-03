from maindash import appplication
from layout import make_layout

appplication.layout = make_layout
appplication.title = "Sentiment of the news regarding the Israel-Hamas war"
appplication._favicon = "favico.ico"

server = appplication.server
# def create_app():
#     from maindash import appplication
#
#     appplication.layout = make_layout
#     appplication.title = "Sentiment of the news regarding the Israel-Hamas war"
#     appplication._favicon = "favico.ico"
#     return appplication


if __name__ == "__main__":
    # app_ = create_app()
    appplication.run_server(debug=True)