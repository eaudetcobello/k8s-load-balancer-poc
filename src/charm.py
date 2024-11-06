#!/usr/bin/env python3
# Copyright 2024 Ubuntu
# See LICENSE file for licensing details.

"""Charm the application."""

from dataclasses import dataclass
import logging

import ops
import json
from charms.k8s.v0.k8sd_api_manager import (
    LoadBalancerConfig,
)

logger = logging.getLogger(__name__)

ENDPOINT_NAME = "k8s-load-balancer-feature"

@dataclass
class K8sFeatureConfiguration():
    def __init__(self, feature: str, version: str, attributes: dict[str,str]):
        self.feature = feature
        self.version = version
        self.attributes = attributes


class K8SLoadBalancerCharm(ops.CharmBase):
    """Charm the application."""

    def __init__(self, framework: ops.Framework):
        super().__init__(framework)
        framework.observe(self.on.start, self._on_start)
        framework.observe(
            self.on.config_changed,
            self._on_k8s_load_balancer_feature_changed,
        )

    def _on_k8s_load_balancer_feature_changed(self, _event: ops.RelationEvent):
        """Handle k8s-load-balancer-feature relation event."""
        logger.info("k8s-load-balancer-feature relation event")

        lb_config = LoadBalancerConfig(enabled=True)  # type: ignore

        # set relation data to lb_config
        relation = self.model.get_relation(ENDPOINT_NAME)
        if relation is not None:
            feature_config = K8sFeatureConfiguration(
                feature="load-balancer",
                version="0.2",
                attributes=lb_config.dict(),
            )
            relation.data[self.unit].update({"feature-name": feature_config.feature})
            relation.data[self.unit].update({"feature-version": feature_config.version})
            relation.data[self.unit].update({"feature-attributes": json.dumps(feature_config.attributes)})

    def _on_start(self, _event: ops.StartEvent):
        """Handle start event."""
        self.unit.status = ops.ActiveStatus()


if __name__ == "__main__":  # pragma: nocover
    ops.main(K8SLoadBalancerCharm)  # type: ignore
