
from AggregatedFormatter import AggregatedFormatter
from GenericCategoryLinebreakIndentation import GenericCategoryLinebreakIndentation
from ParameterAfterBlockNewline import ParameterAfterBlockNewline
from HasIncludeSpaceRemover import HasIncludeSpaceRemover
from RemoveVoidBlockDeclaration import RemoveVoidBlockDeclaration
from RemoveAPIAvailableSemicolon import RemoveAPIAvailableSemicolon
from DeferDeprecationsIndentationFix import DeferDeprecationsIndentationFix

if __name__ == "__main__":
    formatters = [
        #GenericCategoryLinebreakIndentation(),
        ParameterAfterBlockNewline(),
        HasIncludeSpaceRemover(),
        RemoveVoidBlockDeclaration(),
        RemoveAPIAvailableSemicolon(),
        DeferDeprecationsIndentationFix(),
    ]
    AggregatedFormatter(formatters).run()
