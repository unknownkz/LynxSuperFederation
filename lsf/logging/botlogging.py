import logging as lsflog

lsflog.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[lsflog.FileHandler("log.txt"), lsflog.StreamHandler()],
    level=lsflog.INFO,
)
LOGGER = lsflog.getLogger(__name__)
