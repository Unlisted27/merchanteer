import components

gold = components.good("gold","shiny",1,0.1)
gold_chest = components.crate(gold,100)
theSliver = components.ship("the Sliver",cargo=[gold_chest])
theSplinter = components.ship("the Splinter",cargo=[gold_chest])
portGrandure = components.port("port Grandure",[theSliver,theSplinter])
portGrandure.manageGoods()