"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

import numpy as np
import pygad
from TDStoreTools import StorageManager
import TDFunctions as TDF


class GeneticExt:
    """
    GeneticExt description
    """

    def __init__(self, ownerComp):
        # The component to which this extension is attached
        self.ownerComp = ownerComp

        self.ga_instance = None
        self.const_latest = op("constant_latest")
        self.const_best = op("constant_best")
        self.FitnessFunc = None

    def Run(self):
        if self.ga_instance is None:
            self.Init()
        self.FitnessFunc = parent().par.Fitness.eval().module.fitness
        assert self.ga_instance is not None, "ga_instance is not set"
        self.ga_instance.run()
        self.push_genes(self.const_latest, self.ga_instance.best_solution()[0])

    def Init(self):
        genes = self.ownerComp.par.Genes.eval()
        mutation_percent = self.ownerComp.par.Mutationpercent.eval()
        generations = self.ownerComp.par.Generations.eval()
        population = self.ownerComp.par.Population.eval()
        range_low = self.ownerComp.par.Range1.eval()
        range_high = self.ownerComp.par.Range2.eval()

        self.ga_instance = pygad.GA(
            num_generations=generations,
            num_parents_mating=2,
            fitness_func=self.fitness,
            sol_per_pop=population,
            num_genes=genes,
            mutation_percent_genes=mutation_percent,
            on_generation=self.on_generation,
            gene_space=[{"low": range_low, "high": range_high}] * genes,
        )

    def on_generation(self, ga_instance: pygad.GA):
        print(f"Generation = {ga_instance.generations_completed}")
        print(f"Best fitness = {ga_instance.best_solution()[1]}")
        print(f"Best solution = {ga_instance.best_solution()[0]}")

    def push_genes(self, chop: CHOP, X: np.ndarray):
        for i, x in enumerate(X):
            chop.par[f"const{i}value"] = x
        chop.cook(force=True)

    def fitness(
        self, ga_instance: pygad.GA, solution: np.ndarray, solution_index: int
    ) -> np.ndarray | list[float] | float:
        assert self.FitnessFunc is not None, "FitnessFunc is not set"
        self.push_genes(self.const_latest, solution)
        return self.FitnessFunc(ga_instance, solution, solution_index)
