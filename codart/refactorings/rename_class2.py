"""
## Introduction

When the name of a class does not explain what the class does (class's functionality), it needs to be changed.

The module implements a light-weight version of Rename Class refactoring described in `rename_class.py`

### Pre-conditions:

Todo: Add pre-conditions

### Post-conditions:

Todo: Add post-conditions


"""


import os
import sys


from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from codart.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from codart.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from codart.gen.javaLabeled.JavaLexer import JavaLexer

sys.path.append('../../')


class RenameClassRefactoringListener(JavaParserLabeledListener):
    """

    The class implements rename class refactoring

    """

    def __init__(self,
                 common_token_stream: CommonTokenStream = None,
                 package_name: str = None,
                 class_identifier: str = None,
                 class_new_name: str = None):

        """
        Args:

            common_token_stream (CommonTokenStream): An instance of ANTLR4 CommonTokenStream class

            package_name(str): Name of the package in which the refactoring has to be done

            class_identifier(str): Name of the class in which the refactoring has to be done

            class_new_name(str): The new name of the refactored class


        Returns:

            RenameMethodListener: An instance of RenameClassRefactoringListener class

        """

        self.token_stream = common_token_stream
        self.class_new_name = class_new_name
        self.class_identifier = class_identifier
        self.package_identifier = package_name

        self.is_package_imported = False
        self.in_selected_package = False
        self.in_selected_class = False
        self.in_some_package = False

        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.in_some_package = True
        if self.package_identifier == ctx.qualifiedName().getText():
            self.in_selected_package = True
            print("Package " + self.package_identifier + " Found")

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        if ctx.getText() == "import" + self.package_identifier + "." + self.class_identifier + ";" \
                or ctx.getText() == "import" + self.package_identifier + ".*" + ";" \
                or ctx.getText() == "import" + self.package_identifier + ";":
            self.is_package_imported = True
            print("package " + self.package_identifier + " imported")
        if ctx.getText() == "import" + self.package_identifier + "." + self.class_identifier + ";":
            self.token_stream_rewriter.replaceIndex(
                index=ctx.qualifiedName().start.tokenIndex + 2 * len(ctx.qualifiedName().IDENTIFIER()) - 2,
                text=self.class_new_name)
            print("class name in package changed")

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_package_imported or self.in_selected_package:
            if ctx.IDENTIFIER().getText() == self.class_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.start.tokenIndex + 2,
                    text=self.class_new_name)
                change_file_name(self.class_identifier, self.class_new_name)
                print("class name : " + self.class_identifier + " in class declaration changed ")

    def enterCreatedName0(self, ctx: JavaParserLabeled.CreatedName0Context):
        if self.is_package_imported or self.in_selected_package:
            if ctx.IDENTIFIER(0).getText() == self.class_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.start.tokenIndex,
                    text=self.class_new_name)
                print("class name in creator changed")

    def enterClassOrInterfaceType(self, ctx:JavaParserLabeled.ClassOrInterfaceTypeContext):
        if self.is_package_imported or self.in_selected_package:
            if ctx.IDENTIFIER(0).getText() == self.class_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.start.tokenIndex,
                    text=self.class_new_name)
                print("class type changed")

    def enterConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        if self.is_package_imported or self.in_selected_package:
            if ctx.IDENTIFIER().getText() == self.class_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.start.tokenIndex,
                    text=self.class_new_name)
                print("constructor name changed !")


old_names = []
new_names = []


def change_file_name(old, new):
    old_names.append(old)
    new_names.append(new)


def main():
    Path = "../../tests/rename_tests/benchmark"
    Package_name = "org.json"
    class_identifier = "CDL"
    new_class_name = "test"

    FolderPath = os.listdir(Path)
    testsPath = os.listdir(Path + "/refactoredFiles/")

    # delete last refactored files
    for t in testsPath:
        os.remove(os.path.join(Path + "/refactoredFiles/", t))

    for File in FolderPath:
        # We have all of the java files in this folder now
        if File.endswith('.java'):
            EachFilePath = Path + "/" + File
            print(" ****************" + " in file : " + File + " ****************")
            EachFile = FileStream(str(EachFilePath))
            FileName = File.split(".")[0]
            Refactored = open(Path + "/refactoredFiles/" + FileName + "_Refactored.java", 'w', newline='')

            Lexer = JavaLexer(EachFile)

            TokenStream = CommonTokenStream(Lexer)

            Parser = JavaParserLabeled(TokenStream)

            Tree = Parser.compilationUnit()

            ListenerForReRenameClass =\
                RenameClassRefactoringListener(TokenStream, Package_name, class_identifier, new_class_name)

            Walker = ParseTreeWalker()

            Walker.walk(ListenerForReRenameClass, Tree)

            Refactored.write(ListenerForReRenameClass.token_stream_rewriter.getDefaultText())

    print("changing public class files name... ")
    for i in range(len(old_names)):
        os.rename(Path + "/refactoredFiles/" + old_names[i] + "_Refactored.java",
                  Path + "/refactoredFiles/" + new_names[i] + "_Refactored.java")

    print(" %%%%%%%%%%%%%" + " all files finished " + "****************")


if __name__ == "__main__":
    main()
