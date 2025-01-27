from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from structlog.stdlib import (
        BoundLogger,
    )
from nomad.config import config
from nomad.datamodel.data import (
    ArchiveSection,
    Schema,
)
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.metainfo import Datetime, Quantity, SchemaPackage, SubSection
from structlog.stdlib import (
    BoundLogger,
)

configuration = config.get_plugin_entry_point(
    'cpfs_preparation_log:schema_package_entry_point'
)


m_package = SchemaPackage()


class CPFSPreparationStep(ArchiveSection):
    date = Quantity(
        type=Datetime,
        description='The date and time the step happened.',
        a_eln=ELNAnnotation(
            component='DateTimeEditQuantity',
        ),
    )
    image_of_step = Quantity(
        type=str,
        description='Images showing the step.',
        a_browser={'adaptor': 'RawFileAdaptor'},
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.FileEditQuantity,
        ),
    )
    description = Quantity(
        type=str,
        description='Any information that cannot be captured in the other fields.',
        a_eln=dict(component='RichTextEditQuantity', props=dict(height=200)),
    )

    def normalize(self, archive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class CPFSPreparationExfoliationStep(CPFSPreparationStep):
    tape_type = Quantity(
        type=str,
        a_eln=ELNAnnotation(
            component='StringEditQuantity',
        ),
    )
    pretreatment = Quantity(
        type=str,
        a_eln=ELNAnnotation(
            component='StringEditQuantity',
        ),
    )

    def normalize(self, archive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class CPFSPreparationTransferStep(CPFSPreparationStep):
    used_polymer = Quantity(
        type=str,
        a_eln=ELNAnnotation(
            component='StringEditQuantity',
        ),
    )
    pickup_temperature = Quantity(
        type=float,
        description="""
        The pickup temperature.
        """,
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'celsius'},
        unit='celsius',
    )

    def normalize(self, archive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SingleContact(ArchiveSection):
    contact_size_x = Quantity(
        type=float,
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'micrometer'},
        unit='micrometer',
    )
    contact_size_x = Quantity(
        type=float,
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'micrometer'},
        unit='micrometer',
    )
    contact_resistance = Quantity(
        type=float,
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'ohm'},
        unit='ohm',
    )

    def normalize(self, archive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class CPFSPreparationContactingStep(CPFSPreparationStep):
    contacts = SubSection(
        section_def=SingleContact,
        repeats=True,
    )

    def normalize(self, archive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class CPFSPreparationLog(Schema):
    name = Quantity(
        type=str, a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity)
    )
    steps = SubSection(
        section_def=CPFSPreparationStep,
        repeats=True,
    )

    def normalize(self, archive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


m_package.__init_metainfo__()
