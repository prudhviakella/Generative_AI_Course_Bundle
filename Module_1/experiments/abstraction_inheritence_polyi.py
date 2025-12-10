"""
🌍 ECOSYSTEM HARMONY SIMULATOR 🌿
An innovative approach to teaching OOP concepts through nature and cooperation

Scenario: You're creating a simulation of a thriving ecosystem where different
organisms coexist peacefully, each contributing to the balance of nature.
"""

from abc import ABC, abstractmethod
from typing import List


# ================================
# 🎯 CONCEPT 1: INTERFACE/ABSTRACT CLASS
# ================================
# Think of this as "NATURE'S BLUEPRINT"
#
# Real-world analogy:
# - All living things must breathe, consume energy, and reproduce
# - But HOW they do it varies - fish breathe through gills, humans through lungs
#
# In ecosystem terms:
# - Every organism MUST interact with its environment
# - But a tree interacts differently than a bee

class LivingOrganism(ABC):
    """
    🌱 NATURE'S CONTRACT: Every living organism must follow these patterns

    This is an INTERFACE - a natural law that says:
    "If you want to be part of this ecosystem, you must perform these life functions"
    """

    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species
        self.energy = 100
        self.age = 0
        self.contributions: List[str] = []

    @abstractmethod
    def produce_energy(self) -> str:
        """Every organism must obtain energy - but methods vary"""
        pass

    @abstractmethod
    def contribute_to_ecosystem(self) -> str:
        """Every organism contributes something unique to the ecosystem"""
        pass

    @abstractmethod
    def communicate(self) -> str:
        """Every organism has a way to communicate or signal"""
        pass

    @abstractmethod
    def adapt_to_season(self, season: str) -> str:
        """Every organism responds to seasonal changes"""
        pass

    # 🎁 CONCRETE METHOD - Already implemented, available to everyone
    def rest(self) -> str:
        """
        This is NOT abstract - it's already working code!
        All organisms rest to conserve energy.
        But they CAN override it if they need something special.
        """
        self.energy = min(100, self.energy + 20)
        return f"😌 {self.name} is resting peacefully. Energy restored to {self.energy}"

    def grow(self) -> str:
        """All organisms grow with time"""
        self.age += 1
        return f"🌱 {self.name} has grown! Age: {self.age} cycles"

    def status(self) -> str:
        """Show organism status"""
        return f"📊 {self.name} ({self.species}) | Energy: {self.energy} | Age: {self.age} | Contributions: {len(self.contributions)}"


# ================================
# 🎯 CONCEPT 2: INHERITANCE (Single Level)
# ================================
# Think of it as EVOLUTIONARY TRAITS
#
# Real-world analogy:
# - All plants share basic traits (photosynthesis, rooting)
# - But each plant family has unique characteristics
#
# In ecosystem terms:
# - Plants inherit from LivingOrganism (they need energy, grow, age)
# - But Plants add their own unique traits (chlorophyll, root depth)

class Plant(LivingOrganism):
    """
    🌳 PLANT KINGDOM - Inherits from LivingOrganism

    INHERITANCE means:
    - Gets everything from LivingOrganism (energy, age, rest, grow)
    - Adds new plant-specific features (chlorophyll, roots, photosynthesis)
    - MUST implement all abstract methods from parent
    """

    def __init__(self, name: str, species: str):
        super().__init__(name, species)
        self.chlorophyll_level = 100
        self.root_depth = 10
        self.oxygen_produced = 0

    def produce_energy(self) -> str:
        """Plants create energy through photosynthesis"""
        self.energy += 15
        self.oxygen_produced += 10
        return f"☀️ {self.name} performs photosynthesis! Energy: {self.energy}, O₂ produced: {self.oxygen_produced}"

    def contribute_to_ecosystem(self) -> str:
        """Plants provide oxygen and shelter"""
        contribution = f"Oxygen production (+{self.oxygen_produced} units)"
        self.contributions.append(contribution)
        return f"🌿 {self.name} releases fresh oxygen and provides habitat for creatures"

    def communicate(self) -> str:
        """Plants communicate through chemical signals"""
        return f"🍃 {self.name} releases aromatic compounds to signal nearby plants"

    def adapt_to_season(self, season: str) -> str:
        """Plants adapt their growth based on seasons"""
        if season == "spring":
            return f"🌸 {self.name} blooms with vibrant flowers!"
        elif season == "summer":
            return f"🌞 {self.name} grows lush leaves and deepens roots"
        elif season == "autumn":
            return f"🍂 {self.name} stores nutrients and prepares for dormancy"
        else:  # winter
            return f"❄️ {self.name} enters dormant state, conserving energy"


class Pollinator(LivingOrganism):
    """
    🐝 POLLINATOR FAMILY - Another child of LivingOrganism

    Same parent, but COMPLETELY different implementation!
    This shows how inheritance allows diversity while maintaining structure.
    """

    def __init__(self, name: str, species: str):
        super().__init__(name, species)
        self.pollen_collected = 0
        self.flowers_visited = 0
        self.flight_range = 100

    def produce_energy(self) -> str:
        """Pollinators gather energy from nectar"""
        if self.energy < 80:
            self.energy += 20
            self.flowers_visited += 1
            return f"🌺 {self.name} sips sweet nectar from flowers! Energy: {self.energy}"
        return f"✨ {self.name} has sufficient energy"

    def contribute_to_ecosystem(self) -> str:
        """Pollinators enable plant reproduction"""
        contribution = f"Pollinated {self.flowers_visited} flowers"
        self.contributions.append(contribution)
        self.pollen_collected += 5
        return f"🌼 {self.name} spreads pollen, helping plants reproduce! Pollen: {self.pollen_collected}"

    def communicate(self) -> str:
        """Pollinators communicate through dance and signals"""
        return f"💃 {self.name} performs a waggle dance, sharing flower locations with the colony!"

    def adapt_to_season(self, season: str) -> str:
        """Pollinators adjust activity based on seasons"""
        if season == "spring":
            return f"🌸 {self.name} emerges energetically - flowers are blooming!"
        elif season == "summer":
            return f"☀️ {self.name} works tirelessly during peak bloom season"
        elif season == "autumn":
            return f"🍂 {self.name} gathers extra resources for the cold months"
        else:  # winter
            return f"🏠 {self.name} stays in the hive/nest, keeping warm with the colony"


# ================================
# 🎯 CONCEPT 3: MULTI-LEVEL INHERITANCE
# ================================
# Think of it as SPECIALIZED EVOLUTION
#
# Real-world analogy:
# - Life -> Plants -> Trees -> Ancient Trees (multiple evolutionary steps)
# - Each generation adds more specialized adaptations
#
# In ecosystem terms:
# - Ancient trees are highly specialized plants
# - They inherit from Plant, who inherited from LivingOrganism
# - They have centuries of accumulated wisdom and ecosystem importance

class AncientTree(Plant):
    """
    🌲 ANCIENT TREE - Inherits from Plant (who inherits from LivingOrganism)

    MULTI-LEVEL INHERITANCE (3 levels):
    LivingOrganism -> Plant -> AncientTree

    Ancient Trees get:
    - Everything from LivingOrganism (energy, age, rest, grow)
    - Everything from Plant (chlorophyll, photosynthesis, roots)
    - Plus their own ancient features (wisdom, massive size, ecosystem anchoring)
    """

    def __init__(self, name: str, species: str, centuries_old: int):
        super().__init__(name, species)
        self.centuries_old = centuries_old
        self.wisdom_level = centuries_old * 10
        self.root_depth = 100  # Much deeper than regular plants
        self.canopy_size = centuries_old * 5
        self.creatures_sheltered = 0

    def produce_energy(self) -> str:
        """
        🎯 RUNTIME POLYMORPHISM EXAMPLE #1

        This is METHOD OVERRIDING:
        - AncientTree has its OWN version of produce_energy()
        - When you call ancient_tree.produce_energy(), THIS version runs
        - NOT the Plant version, NOT the LivingOrganism version

        The decision happens at RUNTIME based on the actual object type
        """
        self.energy += 25  # Ancient trees are more efficient
        self.oxygen_produced += 50  # Much more oxygen production
        self.creatures_sheltered += 3
        return f"🌳 {self.name} ({self.centuries_old} centuries) produces abundant energy! O₂: +{self.oxygen_produced}, Sheltering: {self.creatures_sheltered} creatures"

    def contribute_to_ecosystem(self) -> str:
        """
        🎯 RUNTIME POLYMORPHISM EXAMPLE #2

        Ancient trees contribute MORE than regular plants
        Same method name, enhanced behavior - that's polymorphism!
        """
        contribution = f"Massive oxygen ({self.oxygen_produced}), shelter ({self.creatures_sheltered}), wisdom"
        self.contributions.append(contribution)
        return f"🏛️ {self.name} serves as an ecosystem anchor - providing shelter, oxygen, and wisdom to all"

    def communicate(self) -> str:
        """Ancient trees communicate through vast root networks"""
        return f"🌐 {self.name} shares nutrients and warnings through the 'Wood Wide Web' - underground root network"

    def share_wisdom(self) -> str:
        """NEW method - only Ancient Trees can do this"""
        return f"📚 {self.name} whispers ancient knowledge through rustling leaves - {self.wisdom_level} wisdom accumulated over {self.centuries_old} centuries"

    def adapt_to_season(self, season: str) -> str:
        """Ancient trees have witnessed countless seasons"""
        base_adaptation = super().adapt_to_season(season)
        return f"{base_adaptation} - Having witnessed {self.centuries_old * 400} seasons, {self.name} stands resilient"


# ================================
# 🎯 CONCEPT 4: RUNTIME POLYMORPHISM
# ================================
# Think of it as "NATURE'S DIVERSITY"
#
# Real-world analogy:
# - Ask 3 organisms "How do you survive winter?"
#   - Bear: "I hibernate in a cave"
#   - Bird: "I migrate to warmer climates"
#   - Tree: "I go dormant and drop my leaves"
# - SAME challenge, DIFFERENT solutions based on WHAT you are
#
# In programming:
# - The program decides WHICH method to call at RUNTIME
# - Based on the ACTUAL object type, not the variable type

class MushroomNetwork(Plant):
    """
    🍄 MUSHROOM NETWORK - Specialized decomposer showing polymorphism

    Inherits from Plant but behaves VERY differently
    Perfect example of polymorphism - same interface, different implementation
    (Note: Fungi aren't technically plants, but for teaching purposes we'll use this hierarchy)
    """

    def __init__(self, name: str, species: str):
        super().__init__(name, species)
        self.mycelium_network = 0  # Underground network size
        self.nutrients_recycled = 0
        self.connections_formed = 0
        self.chlorophyll_level = 0  # Mushrooms don't have chlorophyll!

    def produce_energy(self) -> str:
        """
        🎯 POLYMORPHISM: Completely different energy production

        Even though it's called "produce_energy" like the parent,
        mushrooms don't photosynthesize - they decompose!
        """
        self.energy += 10
        self.nutrients_recycled += 20
        return f"🍄 {self.name} breaks down organic matter into nutrients! Recycled: {self.nutrients_recycled} units"

    def contribute_to_ecosystem(self) -> str:
        """🎯 POLYMORPHISM: Unique decomposer role"""
        contribution = f"Recycled {self.nutrients_recycled} nutrients, network size: {self.mycelium_network}"
        self.contributions.append(contribution)
        return f"♻️ {self.name} transforms decay into life - recycling nutrients for the entire forest!"

    def communicate(self) -> str:
        """🎯 POLYMORPHISM: Mushrooms have incredible communication networks"""
        self.connections_formed += 2
        return f"🌐 {self.name} connects plants through mycelium network - facilitating resource sharing! Connections: {self.connections_formed}"

    def adapt_to_season(self, season: str) -> str:
        """🎯 POLYMORPHISM: Mushrooms thrive in specific conditions"""
        if season == "spring":
            return f"🌧️ {self.name}'s network expands rapidly in moist spring soil"
        elif season == "summer":
            return f"🌱 {self.name} forms fruiting bodies - mushrooms appear above ground!"
        elif season == "autumn":
            self.mycelium_network += 50
            return f"🍂 {self.name}'s prime season - expanding network to {self.mycelium_network} meters!"
        else:  # winter
            return f"❄️ {self.name}'s network persists underground, protected and patient"

    def connect_organisms(self, org1: str, org2: str) -> str:
        """NEW method - mushrooms create symbiotic networks"""
        self.connections_formed += 1
        return f"🤝 {self.name} facilitates nutrient exchange between {org1} and {org2} through mycelium network"


class CoralReef(LivingOrganism):
    """
    🪸 CORAL REEF - Marine ecosystem builder

    Shows how different organisms can inherit from the same base
    but create entirely different ecosystems
    """

    def __init__(self, name: str, species: str):
        super().__init__(name, species)
        self.polyp_count = 1000
        self.symbiotic_algae = 500
        self.fish_sheltered = 0
        self.calcium_structure = 100

    def produce_energy(self) -> str:
        """Coral gets energy from symbiotic algae"""
        self.energy += 15
        self.symbiotic_algae += 10
        return f"🌊 {self.name}'s algae partners perform photosynthesis underwater! Energy: {self.energy}"

    def contribute_to_ecosystem(self) -> str:
        """Coral creates habitat for thousands of species"""
        self.fish_sheltered += 20
        contribution = f"Sheltering {self.fish_sheltered} marine creatures"
        self.contributions.append(contribution)
        return f"🐠 {self.name} provides home for {self.fish_sheltered} fish and marine life!"

    def communicate(self) -> str:
        """Coral communicates chemically and through colony coordination"""
        return f"💫 {self.name}'s polyps coordinate synchronously - releasing spawn in harmony with lunar cycles"

    def adapt_to_season(self, season: str) -> str:
        """Coral responds to water temperature and light changes"""
        if season == "spring":
            return f"🌸 {self.name} spawns - releasing coral larvae into the currents"
        elif season == "summer":
            return f"☀️ {self.name} grows actively with strong sunlight and warm waters"
        elif season == "autumn":
            return f"🌊 {self.name} maintains steady growth as waters cool"
        else:  # winter
            return f"❄️ {self.name} slows growth but remains vibrant in cooler waters"

    def build_reef(self) -> str:
        """Coral's unique ability to create geological structures"""
        self.calcium_structure += 10
        return f"🏗️ {self.name} secretes calcium carbonate - building reef structure: {self.calcium_structure} units"


# ================================
# 🌍 INTERACTIVE DEMONSTRATION
# ================================

def observe_organism(organism: LivingOrganism, season: str = "spring"):
    """
    🎯 THE MAGIC OF POLYMORPHISM IN ACTION!

    This function observes ANY organism type
    But each organism responds DIFFERENTLY to the same observations!

    This is RUNTIME POLYMORPHISM:
    - We don't know which exact organism type until the program runs
    - Python automatically calls the correct version of each method
    - Same observation protocol, different behaviors based on actual organism type
    """
    print(f"\n{'=' * 70}")
    print(f"🔬 Observing: {organism.name}")
    print(f"{'=' * 70}")
    print(organism.status())
    print(organism.produce_energy())
    print(organism.contribute_to_ecosystem())
    print(organism.communicate())
    print(organism.adapt_to_season(season))
    print(organism.rest())
    print(f"{'=' * 70}\n")


# ================================
# 🎬 THE GRAND DEMONSTRATION
# ================================

print("🌍 WELCOME TO THE ECOSYSTEM HARMONY SIMULATOR 🌿\n")

print("📚 Creating different organisms in our ecosystem...\n")

# Create instances of different organism types
oak_tree = Plant("Grandmother Oak", "Quercus")
honey_bee = Pollinator("Buzz", "Apis mellifera")
ancient_sequoia = AncientTree("Eternal Guardian", "Sequoiadendron giganteum", centuries_old=30)
mycelium = MushroomNetwork("Forest Connector", "Mycelium Network")
coral = CoralReef("Rainbow Haven", "Acropora")

print("🎭 DEMONSTRATION 1: POLYMORPHISM IN ACTION")
print("Watch how the SAME observations produce DIFFERENT results!\n")

# The SAME function, but completely different behavior for each organism!
observe_organism(oak_tree, "spring")
observe_organism(honey_bee, "summer")
observe_organism(ancient_sequoia, "autumn")
observe_organism(mycelium, "autumn")
observe_organism(coral, "spring")

print("\n🎭 DEMONSTRATION 2: INHERITANCE IN ACTION")
print("See how specialized organisms inherit and extend ancestral traits!\n")

# Ancient Tree has everything Plant has, PLUS more
print(f"🌲 Ancient Tree specialized abilities:")
print(ancient_sequoia.share_wisdom())
print(f"Root depth: {ancient_sequoia.root_depth} meters (vs regular plant: {oak_tree.root_depth} meters)")
print(f"Wisdom level: {ancient_sequoia.wisdom_level}")

print(f"\n🍄 Mushroom Network inherited but transformed:")
print(f"Has chlorophyll: {mycelium.chlorophyll_level} (Fungi don't photosynthesize!)")
print(f"Has energy needs: {mycelium.energy} (Inherited from LivingOrganism)")
print(mycelium.connect_organisms("Oak Tree", "Pine Tree"))

print("\n🎭 DEMONSTRATION 3: SYMBIOTIC RELATIONSHIPS")
print("How different organisms cooperate in the ecosystem:\n")


def show_symbiosis(organisms: List[LivingOrganism]):
    """Demonstrate how organisms work together"""
    print("🌐 ECOSYSTEM INTERACTIONS:")
    for org in organisms:
        print(f"\n{org.name} ({org.species}):")
        print(f"  ├─ {org.produce_energy()}")
        print(f"  └─ {org.contribute_to_ecosystem()}")


show_symbiosis([oak_tree, honey_bee, mycelium])

print("\n🎭 DEMONSTRATION 4: SEASONAL CYCLES")
print("How organisms adapt through changing seasons:\n")


def seasonal_cycle(organism: LivingOrganism):
    """
    This function demonstrates polymorphism through seasonal changes:
    - Works with ANY organism type
    - Each responds uniquely to the same seasonal challenges
    - Shows adaptability and diversity
    """
    print(f"\n🌍 {organism.name}'s Year:")
    for season in ["spring", "summer", "autumn", "winter"]:
        print(f"  {season.capitalize()}: {organism.adapt_to_season(season)}")
        organism.grow()


seasonal_cycle(ancient_sequoia)
seasonal_cycle(honey_bee)
seasonal_cycle(mycelium)

print("\n🎭 DEMONSTRATION 5: ECOSYSTEM BALANCE SIMULATION")
print("Creating a thriving, interconnected ecosystem:\n")


def ecosystem_cycle(day: int, organisms: List[LivingOrganism]):
    """Simulate one day in the ecosystem"""
    print(f"\n🌅 Day {day} in the Ecosystem:")
    print("─" * 70)

    for organism in organisms:
        print(f"\n{organism.name}:")
        organism.produce_energy()
        organism.contribute_to_ecosystem()

        if isinstance(organism, AncientTree):
            print(f"  🌳 {organism.share_wisdom()}")
        elif isinstance(organism, MushroomNetwork):
            print(f"  🍄 {organism.connect_organisms('Tree roots', 'Seedlings')}")
        elif isinstance(organism, Pollinator):
            print(f"  🐝 Flowers visited: {organism.flowers_visited}")

        if organism.energy < 50:
            organism.rest()

    print("\n" + "─" * 70)


# Run a 3-day simulation
ecosystem = [oak_tree, honey_bee, ancient_sequoia, mycelium, coral]
for day in range(1, 4):
    ecosystem_cycle(day, ecosystem)
    print(f"\n💚 Ecosystem Health: THRIVING - All organisms in balance!\n")

print("\n" + "=" * 70)
print("🎓 KEY CONCEPTS SUMMARY")
print("=" * 70)

print("""
1️⃣ ABSTRACT CLASS / INTERFACE (LivingOrganism):
   - NATURE'S BLUEPRINT that all organisms must follow
   - Cannot create LivingOrganism directly (it's abstract)
   - Ensures all organisms can produce energy, communicate, contribute
   - Like the fundamental laws of biology

2️⃣ INHERITANCE (Plant/Pollinator/Coral inherit from LivingOrganism):
   - Child organisms GET everything from their evolutionary ancestors
   - Can ADD new features (chlorophyll for plants, wings for pollinators)
   - Can MODIFY inherited traits (different energy production methods)
   - Reflects real evolutionary relationships

3️⃣ MULTI-LEVEL INHERITANCE (AncientTree -> Plant -> LivingOrganism):
   - Inheritance chains across evolutionary steps
   - AncientTree gets features from BOTH Plant and LivingOrganism
   - Each level adds specialization and refinement
   - Like evolution: simple -> complex -> highly specialized

4️⃣ RUNTIME POLYMORPHISM (Method Overriding):
   - SAME life function, DIFFERENT implementations
   - Decision made at RUNTIME based on actual organism type
   - ancient_tree.produce_energy() creates MORE than plant.produce_energy()
   - Enables biodiversity while maintaining ecosystem balance
   - Nature's way of creating variety within universal laws

💡 WHY THIS MATTERS IN REAL SOFTWARE:
   - Write ONE observe_organism() that works with ALL organism types
   - Add NEW organisms without changing existing ecosystem code
   - Maintain consistent interfaces while allowing specialization
   - Just like nature creates diversity within consistent physical laws!

🌍 PEACEFUL PRINCIPLES DEMONSTRATED:
   - Cooperation over competition (symbiotic relationships)
   - Diversity creates strength (many organisms, one ecosystem)
   - Balance and harmony (all contribute, all benefit)
   - Sustainable systems (organisms support each other)
   - Ancient wisdom (learning from long-established patterns)
""")

print("=" * 70)
print("🌿 END OF ECOSYSTEM HARMONY SIMULATION 🌍")
print("Thank you for exploring nature's peaceful wisdom through code! 🙏")
print("=" * 70)