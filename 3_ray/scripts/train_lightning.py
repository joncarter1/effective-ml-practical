"""Example of training with PyTorch Lightning."""
import lightning as L
import hydra
import logging
from omegaconf import DictConfig
from lightning.pytorch.callbacks import TQDMProgressBar

from lightning_utils import LitModel, AIMSDataModule

logger = logging.getLogger(__name__)


@hydra.main(config_path="config", config_name="main", version_base=None)
def main(cfg: DictConfig):
    # Init DataModule
    dm = AIMSDataModule(cfg)
    # Init model from datamodule's attributes
    model = LitModel(cfg)
    # Init trainer
    trainer = L.Trainer(
        max_epochs=cfg.train.epochs,
        accelerator="auto",
        devices="auto",
        log_every_n_steps=100,
        callbacks=[TQDMProgressBar(refresh_rate=cfg.train.refresh_rate)],
    )
    # Train
    trainer.fit(model, dm)
    # Test
    trainer.test(model, dm)


if __name__ == "__main__":
    main()
