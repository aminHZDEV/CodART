"""

"""

__version__ = '0.1.0'
__author__ = 'Morteza'

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.java.JavaParser import JavaParser
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class MakeFieldNonFinalRefactoringListener(JavaParserLabeledListener):
    """
    ## Introduction

    Remove the "final" property from a field, so that it can be changed after initialization.

    ## Pre and Post Conditions

    ### Pre Conditions:

    1. User must enter the field's name and the name of the source class in order to make it non-final

    2. Check if the field exists, then make it non-final

    ### Post Conditions:

    No specific Post Condition

    """

    def __init__(self, common_token_stream: CommonTokenStream = None, source_class=None, field_name: str = None):
        """The Main listener which parses the file based on the provided information,
           using ANTLR parser generator and tokenization methods.
           Detects the desired field and removes the "final" keyword from its properties.

           Args:
               common_token_stream (CommonTokenStream): A stream of tokens generated by parsing the main file using the ANTLR parser generator

               source_class (str): Name of the class in which the refactoring has to be done

               field_name (str):Name of the field whose final status has to be changed

            Returns:
                No returns
        """
        if field_name is None:
            self.field_name = ""
        else:
            self.field_name = field_name

        if source_class is None:
            self.source_class = ""
        else:
            self.source_class = source_class
        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        self.is_source_class = False
        self.is_final = False

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):

        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.source_class:
            self.is_source_class = True
        else:
            self.is_source_class = False

    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):

        if not self.is_source_class:
            return None
        grand_parent_ctx = ctx.parentCtx.parentCtx
        field_identifier = ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().IDENTIFIER().getText()
        print("field_identifier :", field_identifier)
        if self.field_name in field_identifier:

            if not (grand_parent_ctx.modifier() == []):
                for i in range(0, len(grand_parent_ctx.modifier())):
                    if grand_parent_ctx.modifier(i).getText() == "final":
                        self.is_final = True
                        break
                print("-----------------------", self.is_final)
                if self.is_final:
                    self.token_stream_rewriter.replaceRange(
                        from_idx=grand_parent_ctx.modifier(i).start.tokenIndex,
                        to_idx=grand_parent_ctx.modifier(i).stop.tokenIndex,
                        text=''
                    )


if __name__ == '__main__':
    db_path = "/home/ali/Documents/compiler/Research/xerces2-j/xerces2-j.udb"
    class_name = "DesignDoc"
    field_name = "GENERATOR_NAME"
    main_file = ""

    db = und.open(db_path)
    for cls in db.ents("class"):
        if cls.simplename() == class_name:
            if cls.kindname() != "Unknown Class":
                main_file = cls.parent().longname()

    stream = FileStream(main_file, encoding='utf8', errors='ignore')
    # Step 2: Create an instance of AssignmentStLexer
    lexer = JavaLexer(stream)
    # Step 3: Convert the input source into a list of tokens
    token_stream = CommonTokenStream(lexer)
    # Step 4: Create an instance of the AssignmentStParser
    parser = JavaParser(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    my_listener = MakeFieldNonFinalRefactoringListener(common_token_stream=token_stream, source_class=class_name,
                                                       field_name=field_name)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open(main_file, mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())
    db.close()
