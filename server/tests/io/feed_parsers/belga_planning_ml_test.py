import os
import lxml.etree

from belga.io.feed_parsers.belga_planning_ml import BelgaPlanningMLParser
from tests import TestCase


class BelgaPlanningMLTestCase(TestCase):
    filename = "belga_planning_ml.xml"
    parser = BelgaPlanningMLParser()

    def fixture(self):
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, "../fixtures", self.filename))
        with open(fixture, "r") as f:
            return self.load(f)

    def load(self, _file):
        return lxml.etree.parse(_file)

    def parse(self):
        xml = self.fixture()
        self.item = self.parser.parse(xml.getroot(), {"name": "test"})[0]

    def setUp(self):
        super().setUp()
        self.parse()

    def test_parser(self):
        assert self.item is not None
        assert len(self.item["coverages"]) == 2
        assert self.item["item_class"] == "plinat:newscoverage"
        assert self.item["planning_date"].isoformat() == "2025-05-05T22:00:00+00:00"
        assert self.item["event_item"] == "urn:event:123"

        assert self.item["coverages"][0]["planning"]["internal_note"] == "John"
        assert self.item["coverages"][0]["planning"]["ednote"] == "Planned coverage"
        assert self.item["coverages"][0]["planning"]["g2_content_type"] == "text"
        assert (
            self.item["coverages"][0]["planning"]["scheduled"].isoformat()
            == "2025-05-05T22:00:00+00:00"
        )
        assert self.item["coverages"][0]["news_coverage_status"] == {
            "name": "coverage intended",
            "qcode": "ncostat:int",
            "label": "Planned",
        }
        assert self.item["coverages"][1]["news_coverage_status"] == {
            "name": "coverage not decided yet",
            "qcode": "ncostat:notdec",
            "label": "On merit",
        }
