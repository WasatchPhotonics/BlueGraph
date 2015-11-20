""" GUI component tests for bluegraph application
"""
        
from bluegraph import views

class TestBasicGraphInterface:
    def test_label_is_available_on_fedora_and_xvfb(self, qtbot):

        form = views.Basic()

        assert form.lblInfo.text() == "Default"
        assert form.width() == 800
        assert form.height() == 600

class TestPixmapBackedGraph:
    def test_graph_starts_with_default_text(self):
        form = views.PixmapBackedGraph()
        assert form.graphback.title.text() == "BLUE GRAPH"

    def test_graph_starts_with_default_icon(self):
        form = views.PixmapBackedGraph()

        icon = form.graphback.icon.boundingRect()
        assert icon.width() == 23
        assert icon.height() == 23 

