"""

"""

try:
    import understand as und
except ImportError as e:
    print(e)
from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class RemoveMethodRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(self, common_token_stream: CommonTokenStream = None, source_class=None, method_name: str = None):

        if method_name is None:
            self.method_name = ""
        else:
            self.method_name = method_name

        if source_class is None:
            self.source_class = ""
        else:
            self.source_class = source_class
        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        self.is_source_class = False
        self.inner_class_count = 0
        self.is_static = False

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):

        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.source_class:
            self.is_source_class = True
        elif self.is_source_class is True:
            self.inner_class_count += 1

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.source_class:
            self.is_source_class = False
        elif self.is_source_class is True:
            self.inner_class_count -= 1

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not self.is_source_class or self.inner_class_count != 0:
            return None
        grand_parent_ctx = ctx.parentCtx.parentCtx
        method_identifier = ctx.IDENTIFIER().getText()
        if self.method_name == method_identifier:
            self.token_stream_rewriter.delete(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=grand_parent_ctx.start.tokenIndex,
                to_idx=grand_parent_ctx.stop.tokenIndex
            )
            self.detected_method = None


if __name__ == '__main__':
    udb_path = '/home/ali/Desktop/code/TestProject/TestProject.udb'
    source_class = "App"
    method_name = "testMethod"
    # initialize with understand
    main_file = ""
    db = und.open(udb_path)
    for cls in db.ents("class"):
        if cls.simplename() == source_class:
            main_file = cls.parent().longname()

    stream = FileStream(main_file, encoding='utf8', errors='ignore')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    my_listener = RemoveMethodRefactoringListener(common_token_stream=token_stream,
                                                  source_class=source_class,
                                                  method_name=method_name)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open(main_file, mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())
    db.close()
