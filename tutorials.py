

welcome = """Welcome to Jonestown!

        You have just inherited a small bakery from your beloved Uncle Bill.
        Before he died you vowed to him that you would keep his business going.
        
        He left the bakery well provisioned for the next few days, but you're
        going to need to build a farm and a mill immediately if you plan on staying in
        business. 

        Don't let Uncle Bill down!
        """

main_display = """Office screen

        This is the Office screen. Here you can see a list of the 
        Businesses you own, and can create new Businesses as well.

        You can use the buttons or hotkeys to navigate.

        There are 4 layers for every financial enterprise: the 
        Business layer, the Unit layer, the Job layer, and the Order 
        layer. 

        """

new_business = """New Business
        
        Here you can create a new Business. Businesses can contain 
        any number of Units but can only access their own cash reserves, 
        so think carefully before starting a second Business.

        If you're sure you want to do this, enter a name for your new 
        Business and give it some cash to get started.

        """

businessData = """Business screen

        The Business is the top layer of the enterprise pyramid. A Business 
        is a collection of Units that share financial resources and can 
        transfer goods between one another.

        Here we can take a look at this Business's production, stock, 
        and employees.

        Below you can see this Business's Units. Units are the second layer 
        of the pyramid. These are the places where work gets done.

        """

new_unit = """New Unit
        
        Here you can create a new Unit. Units are workspaces for your 
        employees. You start the game with a full production line for bread, 
        and the game will automatically hire employees to work for you.

        Assuming you have enough friends, of course.

        """

unitData = """Unit screen

        Units are the second layer of the enterprise pyramid. Units contain 
        associated Jobs, and are your workspace. Here your employees will plant, 
        harvest, craft, store, and sell products.

        Jobs are the third level of the enterprise pyramid.

        Units also contain Markets. This is where you decide what you want to 
        sell every day. Your Unit will then deal with customers for you 
        automatically. Be careful not to sell anything your other Units may need!

        """

new_job = """New Job

        Here you can create a new Job. Jobs hire employees to fulfill tasks that 
        you set them.

        You only need 1 Manager and 1 Porter for each Unit, but production Jobs 
        can hire up to 10 people each. They'll do this automatically, so don't 
        worry about it.

        You already have all the Jobs you need for now, but as your clientele grows
        you'll need to add more.

        """

jobData = """Job screen

        You can set Orders for your Jobs to fulfill every day. The Job's employees 
        will try to make as many of that product as they can, up to the number that 
        you set for them.

        You'll need to have the materials they need for crafting in the Unit's Stock.

        """

new_order = """New Crafting Line

        Here you can create a Crafting line for the Job to attempt to fulfill every 
        day. Make sure the Unit has a good Tech level for the product you're trying 
        to create- you can craft anything anywhere, but not very well.

        Don't worry about Tech levels. Just make bread at Bakeries, okay?

        """

market = """Market
        
        The Market is where you go to sell your wares. You can only sell things you 
        already crafted, obviously. 

        During the Shop period customers will come to your store. Customers can only 
        go to stores they already know about, and will prefer stores that had good 
        prices in the past. Knowledge about your store will slowly spread throughout 
        the community as you and your employees tell your friends and families about 
        your store. They'll in turn tell their friends about you if they have a good 
        experience, so make sure you keep your supplies flowing and your prices low!

        Prices are set automatically based on supply and demand, so make sure you 
        always have enough in stock to satisfy your customers. 

        """
new_transfer = """New Sales Line

        So you want to start selling a new product? Make sure you remember to craft 
        it as well!

        Sales lines control the amount of every product your Unit will try to sell 
        every day.

        """

new_transport = """

        Transports move goods from one Unit to another within the same Business. Your 
        managers will keep track of how much those products cost, including the labor 
        costs of moving them.

        You can set up a new daily Transport line to move a specific amount of goods 
        FROM this Unit to a Unit of your choice.

        """

house = """House

        This is where you live. This where you store the detailed files you keep on 
        everyone you know.

        You can see their profiles here, but keep in mind that profiles contain outdated 
        data.

        """

people_profiles = """People Profiles

        Here is everything you know about everyone you know. Their ages, birthdays, families, 
        needs, and other info is tracked by your character. This information is updated 
        through conversations with other citizens of Jonestown.

        Remember that this information is accurate but outdated.

        """

store_profiles = """Store Profiles

        Here is everything you know about every place you know. Their prices, employees, 
        your past experience of the place, and other info is tracked by your character. This 
        information is updated through conversations with other citizens of Jonestown.

        Remember that this information is accurate but outdated.

        """

manu_profiles = """Factory Profiles

        Factories are where products are made. They overlap with stores, but not every 
        factory is a store. Other than markets they function in exactly the same way as stores,
        and are in fact modeled the same way internally.

        """

church_profiles = """Church Profiles

        You must go to church every Sunday. Everyone does, and anyway, it's important. 

        Here you can see all the churches you know about. If you aren't a member of a church
        already your character will pick from one of these, but you are, so don't worry about
        it.

        """


town = """Town

        This is the town you live in, Jonestown. There are two maps available. The first
        displays the businesses, homes, and churches in the town, and the second shows the
        zoning map of the town. Units can only be built in the appropriate zoning location,
        and you'll want to choose your spot carefully so that you can maximize the number
        of customers you can capture.
        
        Map key:
        Capital letters are occupied locations.
        h- housing. b- business unit. m- mill. f- farm. w- forest. r- river.

        """

tutorials = [welcome, main_display, new_business, businessData, new_unit, unitData, new_job, jobData, new_order, market, new_transfer, house, people_profiles, store_profiles, manu_profiles, church_profiles, town]
