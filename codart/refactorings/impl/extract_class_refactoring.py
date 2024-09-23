
from codart.refactorings.abstraction import Refactoring
import pandas as pd
import re
class ExtractClass(Refactoring):
    def __init__(self, name, granularity):
        super().__init__(name=name, granularity=granularity)

    def detect_smell(self, *args, **kwargs) -> bool:
        # Implement logic to detect God class or large class smell
        # Parse the Java code and analyze the class to determine if it needs refactoring
        _db = und.open(self.udb_path)
        god_classes = pd.read_csv(config.GOD_CLASS_PATH, sep="\t")
        candidates = []
        for index, row in god_classes.iterrows():
            moved_fields, moved_methods = [], []
            # print(row[0].strip())
            try:
                class_file = _db.lookup(re.compile(row[0].strip() + r'$'), "Class")[0].parent().longname()
                # print(class_file)
            except:
                # print('Class file not found')
                continue
            source_class = row[0].split(".")[-1]
            data = row[1][1:-1]  # skip [ and ]
            data = data.split(",")
            for field_or_method in data:
                field_or_method = field_or_method.strip()
                if "(" in field_or_method:
                    # Method
                    moved_methods.append(
                        field_or_method.split("::")[1].split("(")[0]
                    )
                elif len(field_or_method.split(" ")) == 2:
                    # Field
                    moved_fields.append(
                        field_or_method.split(" ")[-1]
                    )
            candidates.append(
                {
                    "source_class": source_class,
                    "moved_fields": moved_fields,
                    "moved_methods": moved_methods,
                    "file_path": class_file
                }
            )
        # print(candidates)
        # quit()
        _db.close()
        return candidates

        return True

    def identify_opportunities(self, *args, **kwargs) -> bool:
        # Identify fields and methods that can be moved to a new class
        return True

    def check_precondition(self, *args, **kwargs) -> bool:
        # Ensure that the refactoring is applicable (e.g., class has enough code to extract)
        return True

    def apply_refactoring(self, udb_path: str = "", file_path: str = "", *args, **kwargs) -> bool:
        # Perform the actual refactoring
        input_stream = FileStream(file_path)
        lexer = JavaLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = JavaParser(stream)
        tree = parser.compilationUnit()  # or another relevant rule

        # Implement a listener or visitor to modify the AST and apply the refactoring
        listener = YourCustomListener()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        # Output the refactored code back to the file or another output stream
        with open(file_path, 'w') as file:
            file.write(str(tree))  # Serialize the modified tree back to Java code

        return True

    def check_post_condition(self, *args, **kwargs) -> bool:
        # Verify that the refactoring did not break the code (e.g., compile the code, run tests)
        return True