# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import GameGenre, Base, Game, User

engine = create_engine('sqlite:///categories.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Meng", email="mluo.bupt@gmail.com",
             picture='http://mengluo.github.io/me/pics/Avatar.png')
session.add(User1)
session.commit()


# action game genre
gameGenre1 = GameGenre(name="Action Games")

session.add(gameGenre1)
session.commit()

game1 = Game(user_id=1, name="Street Fighter", description="""Commonly abbreviated as SF or Suto, is a fighting video game franchise developed and published by Capcom. The first game in the series was released in 1987. Since then, five other main series games, as well as various spin-offs and crossovers, have been released. Street Fighter II is credited with establishing many of the conventions of the one-on-one fighting genre. The game's playable characters originate from different countries around the world, each with a unique fighting style.""", game_genre=gameGenre1)

session.add(game1)
session.commit()


game2 = Game(user_id=1, name="Call of Duty", description="""Call of Duty is a first-person shooter video game developed by Infinity Ward and published by Activision. It is the first of many installments in the Call of Duty franchise, released on October 29, 2003, for Microsoft Windows. The game simulates infantry and combined arms warfare of World War II using a modified version of the id Tech 3 engine. Much of its theme and gameplay is similar to the Medal of Honor series; however, Call of Duty showcases multiple viewpoints staged in the British, American, and Soviet theaters of World War II.""",
              game_genre=gameGenre1)

session.add(game2)
session.commit()


# adventure game genre
gameGenre2 = GameGenre(name="Adventure Games")

session.add(gameGenre2)
session.commit()

game1 = Game(user_id=1, name="Syberia", description="""Syberia is a graphic adventure developed and published by Microids. It follows protagonist Kate Walker as she attempts to wrap up a sale on behalf of her law firm and travels across Europe and Russia.In addition to the main plot, the game contains a subplot conducted via calls received on Kate's cell phone. It involves Kate's deteriorating relationship with her fiance.""",
              game_genre=gameGenre2)

session.add(game1)
session.commit()


game2 = Game(user_id=1, name="Resident Evil", description="""Resident Evil, known in Japan as Biohazard, is a media franchise created by Shinji Mikami and Tokuro Fujiwara and owned by the Japanese video game company Capcom. The franchise focuses on a series of survival horror games but also incorporates a series of live-action films, animations, comic books, novels, audio dramas, and merchandise. The story follows outbreaks of zombies and other monsters created mainly by the Umbrella Corporation.""", game_genre=gameGenre2)

session.add(game2)
session.commit()

# role-playing game genre
gameGenre3 = GameGenre(name="Role-playing Games")

session.add(gameGenre3)
session.commit()

game1 = Game(user_id=1, name="The Witcher", description="""The Witcher is an action role-playing game developed by CD Projekt Red and published by Atari, based on the novel series of The Witcher by Polish author Andrzej Sapkowski. The story takes place in a medieval fantasy world and follows Geralt of Rivia, one of a few traveling monster hunters who have supernatural powers, known as Witchers. The game's system of moral choices as part of the storyline was noted for its time-delayed consequences and lack of black-and-white morality.""", game_genre=gameGenre3)

session.add(game1)
session.commit()


game2 = Game(user_id=1, name="Minecraft", description="""Minecraft is a sandbox video game created and designed by Swedish game designer Markus "Notch" Persson, and later fully developed and published by Mojang. The creative and building aspects of Minecraft allow players to build with a variety of different cubes in a 3D procedurally generated world. Other activities in the game include exploration, resource gathering, crafting, and combat.""",
              game_genre=gameGenre3)

session.add(game2)
session.commit()

# simulators genre
gameGenre4 = GameGenre(name="Simulator Games")

session.add(gameGenre4)
session.commit()

game1 = Game(user_id=1, name="The Sims", description="""The games in The Sims series are largely sandbox games, in that they lack any defined goals (except for some later expansion packs and console versions which introduced this gameplay style). The player creates virtual people called "Sims" and places them in houses and helps direct their moods and satisfy their desires. Players can either place their Sims in pre-constructed homes or build them themselves. Each successive expansion pack and game in the series augmented what the player could do with their Sims.""", game_genre=gameGenre4)

session.add(game1)
session.commit()


game2 = Game(user_id=1, name="Euro Truck Simulator", description="""Euro Truck Simulator (known as Big Rig Europe in North America) is a 2008 truck simulation game developed and published by SCS Software, set in Europe. The player can drive across a depiction of Europe, visiting its cities, picking up a variety of cargos, and delivering them. Over 300,000 copies of the game have been sold in Europe. Its followup, Euro Truck Simulator 2, was released in 2012.""",
              game_genre=gameGenre4)

session.add(game2)
session.commit()

# strategy game genre
gameGenre5 = GameGenre(name="Strategy Games")

session.add(gameGenre5)
session.commit()

game1 = Game(user_id=1, name="Starcraft", description="""StarCraft is a military science fiction media franchise, created by Chris Metzen and James Phinney and owned by Blizzard Entertainment. The game series, set in the beginning of the 26th century, centers on a galactic struggle for dominance among four species in a distant part of the Milky Way galaxy known as the Koprulu Sector. The player views the events as a military commander for each of the three species. In addition, two spin-off titles have been released; these are authorized expansion packs to the original which focus on other characters and settings based at the same time as the main storyline.""", game_genre=gameGenre5)

session.add(game1)
session.commit()


game2 = Game(user_id=1, name="Euro Truck Simulator", description="""League of Legends (abbreviated LoL) is a multiplayer online battle arena video game developed and published by Riot Games for Microsoft Windows and macOS. The game follows a freemium model and is supported by microtransactions, and was inspired by the Warcraft III: The Frozen Throne mod, Defense of the Ancients. Players assume the role of an unseen "summoner" that controls a "champion" with unique abilities and battle against a team of other players or computer-controlled champions.""", game_genre=gameGenre5)

session.add(game2)
session.commit()

# sports game genre
gameGenre6 = GameGenre(name="Sports Games")

session.add(gameGenre6)
session.commit()

game1 = Game(user_id=1, name="DiRT Rally", description="""Dirt Rally is a racing video game focused on rallying. Players compete in timed stage events on tarmac and off-road terrain in varying weather conditions. On release, the game featured 17 cars, 36 stages from three real world locations - Monte Carlo, Powys and Argolis - and asynchronous multiplayer.[4] Stages range from 4 to 16 km.""",
game_genre=gameGenre6)
session.add(game1)
session.commit()


game2 = Game(user_id=1, name="NBA 2K17", description="""NBA 2K17, is based on the sport of basketball; more specifically, it simulates the experience of the National Basketball Association (NBA). Several game modes are included, such as MyCareer, where the player creates a customizable player and plays through their career, MyGM and MyLeague, both franchise modes where the player controls an entire organization, and MyTeam, where the player creates a team to compete against other players' teams.""", game_genre=gameGenre6)

session.add(game2)
session.commit()

print "added games!"
