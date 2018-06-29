from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import SportCategory, Base, MenuItem

engine = create_engine('sqlite:///sportmenu.db')
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


# Menu for Soccer
sport1 = SportCategory(sport="Soccer")

session.add(sport1)
session.commit()

item1 = MenuItem(name="Soccer Ball", description="High quality materials in the cover, \
backing and bladder help to provide next level match ball performance.\
Thermally bonded, seamless surface for a more predictable flight path, better \
touch, and less water uptake. TSBE technology for a seamless surface with \
better touch and lower water uptake.COVER: Textured TPU",price="$20.50",
                 date='2010-01-23', sport=sport1)
item2 = MenuItem(name="G-form Shin Gaurd", description="This soft, flexible soccer \
shin guard hardens on impact. No hard shell for better comfort, performance, \
and compliance. Lightweight, breathable guard that reduces heat and sweat.\
Combines G-Form's proprietary and patented molded composite constructions\
and designs with a unique integration of XRD Technology to provide the best\
combination of impact protection, comfort and sleeve required.",price="$29.99",
                 date='2012-03-25', sport=sport1)
session.add(item1)
session.add(item2)
session.commit()
# Menu for Hockey
sport2 = SportCategory(sport="Hockey")

session.add(sport2)
session.commit()

item3 = MenuItem(name="Ice Hockey Skates", description="Injected composite \
shell with foam core provides superior stiffness and support during strides \
Microfiber liner with Durazone patches deliver a cushioned instep that reduces\
wear-and-tear Two-piece 7mm felt tongue delivers a soft feel for long-lasting\
comfort Embossed lace-bite guard enhances longevity against pucks and potential\
slashes Semi-flexible tendon guard allows for full stride extension",price="$209\
.99", date='2011-04-28', sport=sport2)
item4 = MenuItem(name="Wood Ice Hockey Stick", description="Stay in control of \
the game with the CCM Junior Edge Ice Hockey Stick. The multi-lam shaft \
construction adds strength and consistency to every shot. A durable, clear \
coat finish maintains the integrity of the shaft surface. \
The fiberglass-reinforced blade ensures durability and reduces vibrations \
while carrying the puck. The variable kick point of this wooden hockey stick \
offers a changing kick point, giving you an edge on the \
competition.",price="$19.99", date='2016-12-14', sport=sport2)
session.add(item3)
session.add(item4)
session.commit()
# Menu for BasketBall 
sport3 = SportCategory(sport="BasketBall")

session.add(sport3)
session.commit()

item5 = MenuItem(name="Official Basketball", description="Cushion Core \
Technology combines low-density sponge rubber and ultra-durable butyl \
rubber, producing a basketball with exceptional feel and unmatched durability. \
Constructed with a microfiber cover that is exclusively designed for the indoor\
court, the Wilson Official Evolution Game Basketball is a \
true champion.",price="$59.99",
                 date='2015-07-21', sport=sport3)
item6 = MenuItem(name="Elite Shooter Sleeve", description="Utilized by the best\
in the game to improve performance, outfit your little sharpshooter with \
the Nike Pro Elite Shooter Sleeve.",price="$15.00",
                 date='2009-05-23', sport=sport3)
session.add(item5)
session.add(item6)
session.commit()
# Menu for Boxing
sport4 = SportCategory(sport="Boxing")

session.add(sport4)
session.commit()

item7 = MenuItem(name="Pro Fight Gloves", description="Compact, lightweight \
and hard-hitting, the new Ringside Ultimate Pro Fight Gloves leave nothing \
to chance, integrating all the features necessary for victory.",price="$125.80",
                 date='2016-10-12', sport=sport4)
item8 = MenuItem(name="Heavy Bag Kit", description="Champions of tomorrow are \
made today. The Ringside Adult Heavy Bag Kit comes with everything you need to \
practice and get an unbeatable workout in the process.",price="$75.59",
                 date='2013-07-30', sport=sport4)
session.add(item7)
session.add(item8)
session.commit()
# Menu for Rugby
sport5 = SportCategory(sport="Rugby")

session.add(sport5)
session.commit()

item9 = MenuItem(name="Headgaurd", description="Rugby headguard offers many \
of the high quality features at an affordable price, ideal for rugby playing \
schools and clubs. Also, IRB approved.",price="$23.50",
                 date='2011-01-27', sport=sport5)
item10 = MenuItem(name="Tackle Bag", description="The Rambo is the largest \
of our Tackle Bag range. Constructed of one piece high density foam and a \
durable, water resistant PVC outer skin.",price="$144.00",
                 date='2000-03-17', sport=sport5)
session.add(item9)
session.add(item10)
session.commit()
# Menu for SnowBoarding
sport6 = SportCategory(sport="SnowBoarding")

session.add(sport6)
session.commit()

item11 = MenuItem(name="Snowboard", description="Aside from the larger-than-life \
design and ultra-firm wood core, the Skunk Ape is like any other Lib Tech Snowb\
oard - awesome. It comes fully equipped with Magne-Traction serrated edge techn\
ology to give riders unmatched grip on hardpack and ice while the C2 BTX profile\
combines the effortless float and playful turning of rocker with the prowess and\
precision of traditional camber.",price="$489.99",
                 date='2009-09-23', sport=sport6)
item12 = MenuItem(name="Snowboard Helmit", description="The helmet embodies \
Bern's thin shell construction, a thin ABS shell aligned with EPS foam \
offering lightweight performance. Other features include a bent bill on the \
front, knit mesh liner with adjustable fit dial on the back, and an audio jack \
with built in speakers in ear flaps.",price="$89.95",
                 date='2008-08-25', sport=sport6)
session.add(item11)
session.add(item12)
session.commit()

print ("added menu items!")
