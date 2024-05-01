"""Example of a PyTorch Lightning model.

https://lightning.ai/docs/pytorch/2.1.0/notebooks/lightning_examples/mnist-tpu-training.html
"""
import lightning as L
import logging
import hydra
import torch
import torch.nn.functional as F
from torch import nn, optim
from torch.utils.data import DataLoader, random_split
from torchmetrics.functional import accuracy
import torchvision as tv

logger = logging.getLogger(__name__)


class AIMSDataModule(L.LightningDataModule):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        transform = tv.transforms.Compose(
            [
                tv.transforms.ToTensor(),
                tv.transforms.Normalize(
                    cfg.dataset.channel_means, cfg.dataset.channel_stds
                ),
            ]
        )
        self.train_val_data: tv.datasets.VisionDataset = hydra.utils.instantiate(
            cfg.dataset.train, transform=transform
        )
        self.test_data: tv.datasets.VisionDataset = hydra.utils.instantiate(
            cfg.dataset.test, transform=transform
        )

    def prepare_data(self):
        ...

    def setup(self, stage=None):
        # Assign train/val datasets for use in dataloaders
        if stage == "fit" or stage is None:
            t_split = int(len(self.train_val_data) * 0.8)
            self.train_data, self.val_data = random_split(
                self.train_val_data, [t_split, len(self.train_val_data) - t_split]
            )

    def train_dataloader(self):
        return DataLoader(
            self.train_data, batch_size=self.cfg.train.batch_size, shuffle=True
        )

    def val_dataloader(self):
        return DataLoader(self.val_data, batch_size=self.cfg.train.batch_size)

    def test_dataloader(self):
        return DataLoader(self.test_data, batch_size=self.cfg.train.batch_size)


class LitModel(L.LightningModule):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.num_classes = cfg.dataset.num_classes
        self.model = hydra.utils.instantiate(cfg.model)
        logger.info(f"Running with model:\n{self.model}")

    def forward(self, x):
        x = self.model(x)
        return F.log_softmax(x, dim=1)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.nll_loss(logits, y)
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.nll_loss(logits, y)
        preds = torch.argmax(logits, dim=1)
        # acc = accuracy(preds, y, task="multiclass", num_classes=self.num_classes)
        self.log("val_loss", loss, prog_bar=True)
        # self.log("val_acc", acc, prog_bar=True)

    def test_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.nll_loss(logits, y)
        preds = torch.argmax(logits, dim=1)
        # acc = accuracy(preds, y, task="multiclass", num_classes=self.num_classes)
        self.log("test_loss", loss, prog_bar=True)
        # self.log("test_acc", acc, prog_bar=True)

    def configure_optimizers(self):
        optimizer: optim.Optimizer = hydra.utils.instantiate(
            self.cfg.optimizer, params=self.model.parameters()
        )
        return optimizer
