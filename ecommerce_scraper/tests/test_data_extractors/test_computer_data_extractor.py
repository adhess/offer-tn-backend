import pytest

from ecommerce_scraper.ecommerce_scraper.factories import make_extractor


@pytest.fixture
def computer_info_extractor(category_factory, db):
    return make_extractor(category=category_factory(name="Computers"))

@pytest.mark.parametrize("text",
                         ["hello"])
def test_screen_size_extracted(text, computer_info_extractor):
    pass


@pytest.mark.parametrize("text",
                         ["hello"])
def test_ssd_extracted(text, computer_info_extractor):
    pass


@pytest.mark.parametrize("text",
                         ["hello"])
def test_hard_disk_extracted(text, computer_info_extractor):
    pass


@pytest.mark.parametrize("text",
                         ["hello"])
def test_cpu_gen_extracted(text, computer_info_extractor):
    pass


@pytest.mark.parametrize("text",
                         ["hello"])
def test_cpu_series_extracted(text, computer_info_extractor):
    pass


@pytest.mark.parametrize("text",
                         ["hello"])
def test_cpu_extracted(text, computer_info_extractor):
    pass


@pytest.mark.parametrize("text",
                         ["hello"])
def test_screen_resolution_extracted(text, computer_info_extractor):
    pass


@pytest.mark.parametrize("text",
                         ["hello"])
def test_ram_extracted(text, computer_info_extractor):
    pass


@pytest.mark.parametrize("text",
                         ["hello"])
def test_ram_type_extracted(text, computer_info_extractor):
    pass


@pytest.mark.parametrize("text",
                         ["hello"])
def test_cpu_frequency_extracted(text, computer_info_extractor):
    pass


@pytest.mark.parametrize("text",
                         ["hello"])
def test_os_extracted(text, computer_info_extractor):
    pass


@pytest.mark.parametrize("text",
                         ["hello"])
def test_warranty_extracted(text, computer_info_extractor):
    pass


@pytest.mark.parametrize("text",
                         ["hello"])
def test_color_extracted(text, computer_info_extractor):
    pass


@pytest.mark.parametrize("text",
                         ["hello"])
def test_gpu_extracted(text, computer_info_extractor):
    pass


@pytest.mark.parametrize("text",
                         ["hello"])
def test_screen_frequency_extracted(text, computer_info_extractor):
    pass


@pytest.mark.parametrize("text",
                         ["hello"])
def test_cpu_cache_extracted(text, computer_info_extractor):
    pass


@pytest.mark.parametrize("text",
                         ["hello"])
def test_reference_extracted(text, computer_info_extractor):
    pass
