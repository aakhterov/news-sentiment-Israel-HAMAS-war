from dash import html


EXPLANATION = html.Div(children=[
    html.H4("Introduction and definitions"),
    html.Div([
        html.Span("We've fine-tuned LLM for performing the BBC LIVE news sentiment analysis "
                  "(you can find the current link to the news feed "),
        html.A("here", href="https://www.bbc.com/news/world/middle_east", target="_blank"),
        html.Span(") related to the Israel-Hamas war which started with the horrific massacre in southern Israel. "
                  "Two sentiments were considered - "),
        html.Span("anti-Israel", className="fw-bold"),
        html.Span(" and "),
        html.Span("pro-Israel", className="fw-bold"),
        html.Span(". Let's state what we mean by anti-Israel news and pro-Israel news. In a few words, "
                  "if a piece of news forms a positive image of Israel, this is pro-Israel news, otherwise, "
                  "this is anti-Israel news. More detail: a piece of news is considered "),
        html.Span("anti-Israel", className="fw-bold"),
        html.Span(" if:"),
        html.Div("1) it's based on the words of Hamas leaders, Gaza ministries, the UN refugee agency "
                 "(UNRWA), or other similar organizations;", className="pt-2"),
        html.Div([
            html.Span("Ex. "),
            html.Span("\"Israeli forces shot dead six Palestinians on Friday at a refugee camp in the north "
                      "of the Israeli-occupied West Bank, the Palestinian health ministry says. It claims "
                      "they were killed at al-Fara camp near Tubas. The Palestinian news agency Wafa says "
                      "several other people were also injured. There has been an increase in violence in "
                      "the West Bank since the Israel-Hamas war began on 7 October. The Israeli military "
                      "spokesperson's office said it was checking the report.\" "),
            html.A("link",
                   href="https://www.bbc.com/news/live/world-middle-east-67653615/page/5?ns_mchannel=social&ns_source=twitter&ns_campaign=bbc_live&ns_linkname=6572c58087855b2dac7d3970%26Palestinian%20health%20ministry%20says%20West%20Bank%20shooting%20leaves%20several%20dead%262023-12-08T08%3A44%3A44.084Z&ns_fee=0&pinned_post_locator=urn:asset:32befc41-cf1a-4643-a72c-420dbb1ec8aa&pinned_post_asset_id=6572c58087855b2dac7d3970&pinned_post_type=share",
                   target="_blank"),
        ], className="fst-italic ps-3"),
        html.Div("2) it says something like \"...10 000 Palestinians have been killed by Israel "
                 "airstrike...\"", className="pt-2"),
        html.Div([
            html.Span("Ex. "),
            html.Span("\"Meanwhile in the West Bank, the death toll from Israeli raids in Jenin overnight "
                      "has risen to eight, the Palestinian health ministry says. The ministry earlier said "
                      "six Palestinians were killed during the raids. Israel's military confirmed it was "
                      "conducting counter-terrorism raids in Jenin and elsewhere in the West Bank, saying "
                      "they had destroyed and confiscated weapons. Since the beginning of the war, more "
                      "than 150 Palestinians including 44 children, have been killed in the West Bank by "
                      "Israeli forces, the UN humanitarian office OCHA says.\" "),
            html.A("link",
                   href="https://www.bbc.co.uk/news/live/world-middle-east-67364296/page/5",
                   target="_blank"),
        ], className="fst-italic ps-3"),
        html.Div("3) it contains statements about immediate ceasefire necessity.", className="pt-2"),
        html.Div([
            html.Span("Ex. "),
            html.Span("\"Liberia has reversed its vote against a humanitarian ceasefire in Gaza following "
                      "a directive by President George Weah. Liberia was the only African nation among the "
                      "10 countries that voted against a humanitarian ceasefire in Gaza during the vote held "
                      "on 12 December. Its diplomats who had voted against the motion had lacked the president's "
                      "approval, the Liberian government said on Wednesday. ""The Liberian Foreign Ministry has "
                      "therefore ensured the reversal of the negative vote through the appropriate channels at "
                      "the United Nations General Assembly and registered a new vote in favour of a ceasefire "
                      "in Gaza,"" authorities said.\" "),
            html.A("link",
                   href="https://www.bbc.com/news/live/world-middle-east-67768062/page/5?ns_mchannel=social&ns_source=twitter&ns_campaign=bbc_live&ns_linkname=65829466b255e96a9e4babe5%26Liberia%20to%20vote%20for%20ceasefire%262023-12-20T07%3A20%3A56.396Z&ns_fee=0&pinned_post_locator=urn:asset:257aa926-6ab7-4094-b19e-9efa80c61cff&pinned_post_asset_id=65829466b255e96a9e4babe5&pinned_post_type=share",
                   target="_blank"),
        ], className="fst-italic ps-3"),

        html.Span("A piece of news is considered ", className="pt-2"),
        html.Span("pro-Israel", className="fw-bold"),
        html.Span(" if:"),
        html.Div("1) It's based on the words of the Israeli official speakers (To be honest "
                 "it's not always right but for simplicity reasons, we've considered it's true).", className="pt-2"),
        html.Div([
            html.Span("Ex. "),
            html.Span("\"Now for an update on Israel's military operation in the north of the Gaza Strip. "
                      "Posting on X, IDF spokesperson Rear Admiral Daniel Hagari says troops destroyed "
                      "buildings and infrastructure at Al-Azhar University which he claims was used "
                      "by Hamas for its military activity. Hagari says an \"underground route that "
                      "leaves the university yard and continues to a school about a kilometre away\" "
                      "was discovered during the raid. Explosive devices, rocket parts and launchers "
                      "were also found, he adds. Hagari says during a separate raid at an observation "
                      "post near the Shatti Hospital, IDF troops found around 200 radios and dozens "
                      "of cameras. \"A combat shaft, cartridges, grenades, a sniper position, military "
                      "equipment and shooting holes"" were also discovered, he adds.\" "),
            html.A("link",
                   href="https://www.bbc.com/news/live/world-middle-east-67653615/page/4?ns_mchannel=social&ns_source=twitter&ns_campaign=bbc_live&ns_linkname=6572fdc769d486126e941676%26IDF%20says%20it%20found%20underground%20Hamas%20infrastructure%20at%20Gaza%20university%262023-12-08T12%3A11%3A29.246Z&ns_fee=0&pinned_post_locator=urn:asset:e4b42dab-1804-4218-9784-1c80597aee90&pinned_post_asset_id=6572fdc769d486126e941676&pinned_post_type=share",
                   target="_blank"),
        ], className="fst-italic ps-3"),
        html.Div("2) It tells about hostages;", className="pt-2"),
        html.Div([
            html.Span("Ex. "),
            html.Span("\"The families of some of those killed and taken hostage from kibbutz Be'eri "
                      "in southern Israel have spoken from the place that that used to be their home. "
                      "\"Until the 6th October this place [Be'eri] was heaven... green grass, flowers, "
                      "birds, children playing with no worries, but on the 7th October this place "
                      "turned into hell,\" Elad says at a news conference. His mother Ofra Keidar, "
                      "70, was kidnapped by Hamas from the kibbutz. ...\" "),
            html.A("link",
                   href="https://www.bbc.com/news/live/world-middle-east-67768062/page/4?ns_mchannel=social&ns_source=twitter&ns_campaign=bbc_live&ns_linkname=6582df94b255e96a9e4bac3e%26Families%20of%20Israeli%20hostages%20speak%20from%20Kibbutz%20%27turned%20into%20hell%27%262023-12-20T14%3A31%3A08.751Z&ns_fee=0&pinned_post_locator=urn:asset:87dbd5d0-cb8a-405e-8793-069264652fa1&pinned_post_asset_id=6582df94b255e96a9e4bac3e&pinned_post_type=share",
                   target="_blank"),
        ], className="fst-italic ps-3"),
        html.Div("3) It tells about Hamas terrorists atrocities.", className="pt-2"),
        html.Div([
            html.Span("Ex. "),
            html.Span("\"Channel 12 news airs a film of some of the victims of the October 7 massacre "
                      "in their final hours at the desert rave in Kibbutz Re’im. Hamas terrorists "
                      "terrorists killed over 260 partygoers as part of the devastating massacre in "
                      "which over 1,400 people were slain, the vast majority civilians. An unknown "
                      "number of partygoers are among the 200-250 people held hostage in Gaza. Some "
                      "of the women who attended the festival were also raped, according to eyewitness "
                      "accounts. The footage — some of it professional and some amateur — is set to "
                      "music without a voiceover, and shows some of those killed and kidnapped as they "
                      "dance and enjoy themselves at the festival, not knowing the carnage that lay ahead...\" "),
            html.A("link",
                   href="https://www.timesofisrael.com/liveblog_entry/footage-shows-october-7-victims-dancing-laughing-at-desert-rave-ahead-of-massacre",
                   target="_blank"),
        ], className="fst-italic ps-3"),
    ], className="ps-2"),
    html.H4("Motivation", className="pt-3"),
    html.Div([
        html.Div("1) Practicing data science frameworks and tools (transformer, Spark, Dash)."),
        html.Div("2) Attempt to get the quantitative estimation of anti-Israeli bias of the "
                 "world-wide news agencies (only the BBC now).")
    ], className="ps-2"),
    html.H4("Implementation details", className="pt-3"),
    html.Div([
        html.Div("1) Fine-tuning the model. For the purpose of this, we used the Hugging Face "
                 "ecosystem and there Python libraries - datasets and transformers. "
                 "The most challenging issue was to create an appropriate dataset."),
        html.Div("1.1) Collect data. From the one hand, there's no annotated dataset that "
                 "fits our goal (at least I couldn't find it). From the other hand, "
                 "it takes a long time to label all data manually. So, we made the following:",
                 className="ps-3"),
        html.Div([
            html.Span("a) we collected and consider as anti-Israel almost all news produced by", className="ps-3"),
            html.A("\"Palestinian News & Information Agency-WAFA\"",
                   href="https://english.wafa.ps/Regions/Details/2", target="_blank", className="ps-3"),
            html.Span("and", className="ps-3"),
            html.A("Al Mayadeen",
                   href="https://english.almayadeen.net", target="_blank", className="ps-3"),
            html.Span("- Lebanese news television channel", className="ps-3")
        ], className="ps-3"),
        html.Div([
            html.Span("b) we collected and consider as pro-Israel almost all news produced by", className="ps-3"),
            html.A("\"The Times of Israel\"",
                   href="https://www.timesofisrael.com", target="_blank", className="ps-3"),
            html.Span("portal.", className="ps-3"),
        ], className="ps-3"),
        html.Div([
            html.Span("c) We annotated a small amount of The BBC LIVE news by hand.", className="ps-3"),
        ], className="ps-3"),
        html.Div([
            html.Span("Corresponding Google Colab notebook can be found "),
            html.A("here", href="https://colab.research.google.com/drive/1zpj-KJDLSz8dATPV3hSxe2Tqj1emB7Ia", target="_blank"),
            html.Span(" and the collected dataset "),
            html.A("here", href="https://huggingface.co/datasets/aav-ds/Israel-HAMAS_war_news", target="_blank"),
        ], className="ps-3"),
        html.Div([
            html.Span("1.2) Annotation data."),
        ], className="ps-3"),
        html.Div([
            html.Span("1.3) Fine-tuning an LLM. We fine-tuned \"DistilBERT base model (uncased)\" "
                      "using Python libarary transformers. Here is "),
            html.A("Google Colab", href="https://colab.research.google.com/drive/11lG-nVzvx9Jm1XUDaEhR2_Qny7ezaDsp#scrollTo=zW1uqT9fNKDu",
                   target="_blank"),
            html.Span(" and "),
            html.A("the model", href="https://huggingface.co/aav-ds/news_sentiment_model", target="_blank"),
        ], className="ps-3"),
        html.Div("2) ETL (Web-scraping - Spark - PostreSQL). For the purpose of collecting a new data "
                 "we use the following ETL pipeline: (1) Python script for scraping the BBC LIVE news, "
                 "predict the sentiment of each news and writing them to the csv files (work in separate "
                 "Docker container and run periodically using cron) -> (2) Spark cluster read the "
                 "created csv files and save the news to the PostgreSQL (work in separate Docker containers)."),
        html.Div("3) Frontend - We use Python libarary Dash for the dashboard implementation "
                 "(also work in separate Docker container)"),
    ], className="ps-2"),
], style={"text-align": "justify"})