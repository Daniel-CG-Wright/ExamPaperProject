# used to specify common exam question criteria.
from typing import Dict
# Stores a dictionary of each topic and its associated key words
# put a ! in front of it to avoid classing it for this string
# e.g. if matching !stock control system then if the only keyword
# is "stock control system" then it will not be matched
TOPICKEYWORDS: Dict[str, str] = {
    "Databases": ["database", "Entity-Relationship Diagram", "ERD"],
    "Contingencies":
    ["contingency", "recovery", "backup"],
    "Operating Systems - buffering, interrupts, polling":
    ["buffering", "polling", "interrupt",
        "buffer", "time slicing", "partitioning", "scheduling"],
    "Operating systems - Modes of operation":
    ["Batch processing", "Real time transaction", "Real time control"],
    "Operating systems - UI, types":
    ["User Interface", "Command Line Interface", "multi-user",
     "multi-processing", "standalone user", "multi-tasking",
     "batch operating system"],
    "Operating systems - resource management":
    ["Utility software", "resource management"],
    "Files":
    ["direct access file", "hash file", "transaction file",
     "master file", "serial file", "sequential file", "fixed length",
     "variable length", "hashing"],
    "Networking":
    ["collision", "Dijkstra",
     "simplex", "duplex", "switch", "router", "network", "LAN", "WAN",
     "internet", "multiplexing", "transmission"],
    "Security":
    ["Biometric", "Encryption", "Malware", "malicious software", "security",
     "validation"],
    "Algorithms":
    ["an algorithm", "passing by reference", "passing by value"],
    "Big O":
    ["Big O", "Time complexity"],
    "Systems":
    ["Safety critical", "weather forecasting",
     "robotics", "CAD", "Computer Aided Design"],
    "Computer architecture":
    ["von neumann", "cache", "control unit"],
    "Assembly language":
    ["Assembly language"],
    "SQL":
    ["SQL"],
    "Data structures":
    ["stack", "queue", "linked list", "two-dimensional array",
     "binary tree"],
    "Binary":
    ["floating point", "fixed point", "two's complement", "binary",
     "masking", "truncation", "rounding"],
    "Processing":
    ["parallel processing", "distributed processing", "data mining"],
    "Code of conduct and legislation and ethics":
    ["code of conduct", "legislation", "ethic"],
    "HCI":
    ["HCI", "interface", "voice input"],
    "Boolean algebra":
    ["Boolean algebra", "De Morgan", "Truth table"],
    "Compression":
    ["compression"],
    "Paradigms":
    ["object", "class", "OOP", "procedural", "paradigm", "languages"],
    "Translation":
    ["Compiler", "interpreter", "assembler", "translation", "compilation"],
    "Software for development":
    ["version control", "IDE", "debugging"],
    "Analysis and design":
    ["waterfall", "agile", "analysis", "feasibility", "investigate",
     "investigation", "changeover"],
    "Backus-Naur":
    ["Backus-Naur", "BNF"],
    "Testing":
    ["Alpha", "beta", "acceptance testing"],
    "Maintenance documentation":
    ["Maintenance documentation"]

}


class CriteriaStruct:

    def __init__(self, topics: set, minmarks: int, maxmarks: int,
                 component: str, level: str,
                 noParts: bool,
                 contentsearch: str = ""):
        """
        Creates a criteria class with topics, minmarks, maxmarks
        etc and an optional contentsearch (for question bank
        use)
        """
        self.topics = topics
        self.minmarks = minmarks
        self.maxmarks = maxmarks
        self.component = component
        self.level = level
        self.noParts = noParts
        self.contentsearch = contentsearch
