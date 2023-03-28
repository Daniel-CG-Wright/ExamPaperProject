# used to specify common exam question criteria.
from typing import Dict
# Stores a dictionary of each topic and its associated key words
# put a ! in front of it to avoid classing it for this string
# e.g. if matching !stock control system then if the only keyword
# is "stock control system" then it will not be matched
TOPICKEYWORDS: Dict[str, str] = {
    "Databases": ["database", "Entity-Relationship Diagram", "ERD"],
    "Software types":
    ["bespoke", "off-the-shelf", "open source", "proprietary"],
    "Contingencies":
    ["contingency", "recovery", "backup"],
    "Operating Systems - buffering, interrupts, polling":
    ["buffering", "polling", "interrupt",
        "buffer", "time slicing", "partitioning", "scheduling"],
    "Operating systems - Modes of operation":
    ["Batch processing", "Real time transaction", "Real time control",
     "mode of operation"],
    "Operating systems - UI, types":
    ["User Interface", "Command Line Interface", "multi-user",
     "multi-processing", "standalone user", "multi-tasking",
     "batch operating system"],
    "Operating systems - resource management":
    ["Utility software", "resource management", "defragmentation",
     "fragmented", "file attributes", "hierarchical"],
    "Files":
    ["direct access file", "hash file", "transaction file",
     "master file", "serial file", "sequential file", "fixed length",
     "variable length", "hashing", "multi-level index", "multi-level indexes",
     "multi level index", "multi level indexes", "file attributes",
     "random access file",
     "random access files", "indexed sequential file",
     "indexed sequential files"],
    "Networking":
    ["collision", "Dijkstra",
     "simplex", "duplex", "switch", "router", "network", "LAN", "WAN",
     "internet", "multiplexing", "transmission", "protocols", "handshaking",
     "shortest path"],
    "Security":
    ["Biometric", "Encryption", "Malware", "malicious software", "security",
     "validation", "cryptography", "threats"],
    "Algorithms":
    ["passing by reference", "passing by value",
     "quicksort", "bubble sort", "insertion sort", "write an algorithm",
     "procedure", "pseudocode", "psuedo-code", "iteration", "recursion",
     "programming constructs"],
    "Big O":
    ["Big O", "Time complexity"],
    "Systems":
    ["Safety critical", "forecasting", "forecast"
     "robotics", "CAD", "Computer Aided Design", "expert system",
     "expert systems"],
    "Computer architecture":
    ["von neumann", "cache", "control unit", "fetch-execute",
     "fetch-decode-execute"],
    "Secondary storage devices":
    ["magnetic disk", "magnetic tape", "optical disk", "optical tape",
     "hdd", "ssd", "optical drive"],
    "Assembly language":
    ["Assembly language"],
    "SQL":
    ["SQL"],
    "Data structures and types":
    ["stack", "queue", "linked list", "two-dimensional array",
     "binary tree", "data type", "data types", "data structure"],
    "Binary":
    ["floating point", "fixed point", "two's complement", "binary",
     "masking", "truncation", "rounding", "two's complementation"],
    "Processing":
    ["parallel processing", "distributed processing", "data mining"],
    "Code of conduct and legislation and ethics":
    ["code of conduct", "legislation", "ethics", "ethical",
     "data protection act", "data protection",
     "computer misuse act", "computer misuse", "protects data"],
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
     "investigation", "changeover", "design review", "evaluation"],
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
