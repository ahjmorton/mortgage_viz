#!/usr/local/bin/python3

from typing import DefaultDict
from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum
from itertools import chain

LinkType = Enum('LinkType', 'dependency phase_task')

@dataclass
class Node:
  name: str
  entity: str
  description: str = ""
  links: dict[str, set[str]] = field(default_factory=dict)

  def dependents(self):
    return self.links.get(LinkType.dependency.name, {})

  def phase_tasks(self):
    return self.links.get(LinkType.phase_task.name, {})

def task(name: str, description: str, dependents: set[str] = set()):
  return Node(
     name=name,
     description=description,
     entity="task",
     links={
       LinkType.dependency.name: frozenset(dependents),
     }
  )

def phase(name: str, description: str, phase_tasks: set[str]):
   return Node(
     name=name,
     description=description,
     entity="phase",
     links={
       LinkType.phase_task.name: frozenset(phase_tasks),
     }
   )

TASKS = [
  task("decide_budget", "Establish a rough budget"),
  task("start_aquiring_deposit", "Begin aquiring your deposit", dependents= {"decide_budget"}),
  task("areas_decided", "Decide on a set of areas"),
  task("property_aspect_decided", "Decide what kind of property"),
  task("search_start", "Start searching for properties", dependents = {"areas_decided", "property_aspect_decided", "decide_budget"}),
  task("aquire_aip", "Aquire an agreement in principle", dependents = {"decide_budget"}),
  task("arrange_viewings", "Start arranging viewings", dependents = {"aquire_aip", "search_start"}),
  task("arrange_second_viewings", "Re-view properties you like", dependents = {"arrange_viewings"}),
  task("have_conveyancers_lined_up", "Have conveyancers ready", dependents = {"arrange_second_viewings"}),
  task("have_advisor_lined_up", "Have mortgage advisor ready", dependents = {"arrange_second_viewings"}),
  task("make_offers", "Make offers on properties you like", dependents = {"arrange_second_viewings", "have_conveyancers_lined_up", "have_advisor_lined_up", "aquire_aip"}),
  task("accept_offer", "Accept sellers offer for a property", dependents = {"make_offers"}),
  task("get_estimated_mortgage_costs", "Have estimated mortgage costs (including furniture)", dependents = {"accept_offer", "have_advisor_lined_up"}),
  task("get_estimated_insurance_quotes", "Get some estimates on insurance quotes", dependents = {"accept_offer", "have_advisor_lined_up"}),
  task("detailed_monthly_estimated_costs", "Get detailed estimated monthly costs", dependents = {"get_estimated_mortgage_costs", "get_estimated_insurance_quotes", "accept_offer"}),
  task("detailed_cost_breakdown", "Have detailed mortgage cost breakdown", dependents = {"accept_offer"}),
  task("decide_on_mortgage", "Decide and submit an application for the mortgage you want", dependents={"detailed_monthly_estimated_costs", "detailed_cost_breakdown"}),
  task("request_a_home_buyers_survey", "Request a homebuyers survey", dependents={"decide_on_mortgage"}),
  task("decide_on_insurance", "Decide and finalise which insurance you want", dependents={"detailed_monthly_estimated_costs"}),
  task("mortgage_application_accepted", "Agree on mortgage offer from the bank", dependents={"decide_on_mortgage"}),
  task("read_home_buyers_survey", "Act on Home buyers survey results", dependents={"request_a_home_buyers_survey", "mortgage_application_accepted"}),
  task("certify_your_documents", "Have certified documents available"),
  task("provide_bank_statements_to_conveyancer", "Provide evidence that the sources of money for your deposit are legitimate", dependents={"start_aquiring_deposit", "mortgage_application_accepted"}),
  task("conveyancer_due_dilligence_done", "Submit all your details to the conveyancer", dependents={"mortgage_application_accepted", "have_conveyancers_lined_up", "certify_your_documents", "provide_bank_statements_to_conveyancer"}),
  task("pay_for_searches", "Pay for searches with Conveyancer", dependents={"conveyancer_due_dilligence_done"}),
  task("get_searches_results", "Searches results received", dependents={"pay_for_searches"}),
  task("chase_up_solicitor", "Inform conveyancer you've submitted your documents", dependents={"conveyancer_due_dilligence_done"}),
  task("follow_up_on_solicitor_enquiries", "Respond to conveyancer enquiries", dependents={"chase_up_solicitor"}),
  task("agree_completion_date_with_sellers", "Agree completion date with sellers", dependents={"get_searches_results", "follow_up_on_solicitor_enquiries"}),
  task("begin_ordering_furniture", "Start buying furniture", dependents={"agree_completion_date_with_sellers"}),
  task("sign_the_contract", "Sign the contract and send it back to the conveyancer for exchange", dependents={"agree_completion_date_with_sellers"}),
  task("begin_arranging_movers", "Arrange movers for your move in date",
    dependents={"agree_completion_date_with_sellers"}
  ),
  task("move_in", "Take ownership of the property e.g. complete", dependents={"sign_the_contract", "begin_arranging_movers"}
  ),
  task("pay_conveyancer", "Pay conveyancer for their services", dependents={"move_in"}),
  task("furnish_your_place", "Accept delivery of your new stuff", dependents={"move_in", "begin_ordering_furniture"})
]

PHASES = [
  phase("planning", "Planning what to buy", phase_tasks = {
    "decide_budget", "start_aquiring_deposit",
    "areas_decided", "property_aspect_decided"
  }),
  phase("searching", "Searching for what to buy", phase_tasks = {
    "search_start", "aquire_aip",
    "arrange_viewings", "arrange_second_viewings",
  }),
  phase("offering", "Offering and getting a mortgage offer", phase_tasks ={
    "have_conveyancers_lined_up", "have_advisor_lined_up",
    "make_offers", "accept_offer",
    "get_estimated_mortgage_costs", "get_estimated_insurance_quotes", 
    "detailed_monthly_estimated_costs", "detailed_cost_breakdown",
    "decide_on_mortgage", "decide_on_insurance",
    "mortgage_application_accepted"
  }),
  phase("conveyance", "Conveyancing", phase_tasks = {
    "certify_your_documents", "request_a_home_buyers_survey",
    "read_home_buyers_survey", "conveyancer_due_dilligence_done",
    "provide_bank_statements_to_conveyancer", 
    "pay_for_searches", "chase_up_solicitor",
    "follow_up_on_solicitor_enquiries", 
    "get_searches_results", "agree_completion_date_with_sellers",

  }),
  phase("exchanging", "Settlement", phase_tasks = {
     "begin_ordering_furniture","sign_the_contract",
     "begin_arranging_movers", "move_in",
     "furnish_your_place", "pay_conveyancer"
  })
]

def main():
  all_task_by_name = {task.name: task for task in TASKS}
  all_phase_tasks = {task_name for phase in PHASES for task_name in phase.phase_tasks()}
  left_over_tasks = [task for task in TASKS if task.name not in all_phase_tasks]
  def as_task_dot(task) : 
    return f'node [label="{task.description}"] {task.name};'
  def as_phase(phase): 
    return "\n".join(chain([
      f'subgraph cluster_{phase.name} {{',
        f'label = "{phase.description}";',
    ],[ as_task_dot(all_task_by_name[task]) for task in phase.phase_tasks()]
     ,[ "}" ]
    ))
  def task_connections(tasks) :
    return [ f'{dependent} -> {task.name};' for task in tasks for dependent in task.dependents()]
  return chain([
    "digraph mortgage {",
      'rankdir="LR";',
  ],map(as_phase, PHASES)
   ,map(as_task_dot, left_over_tasks)
   ,task_connections(TASKS)
   ,[ "}" ]
  )

if __name__ == "__main__":
  print("\n".join(main()))
