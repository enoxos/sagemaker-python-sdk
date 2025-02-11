# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
"""This module contains code to test SageMaker ``DatasetArtifact``"""
from __future__ import absolute_import
from tests.integ.sagemaker.lineage.helpers import traverse_graph_forward


def test_trained_models(
    sagemaker_session,
    dataset_artifact_associated_models,
    trial_component_obj,
    model_artifact_obj1,
):

    model_list = dataset_artifact_associated_models.trained_models()
    for model in model_list:
        assert model.source_arn == trial_component_obj.trial_component_arn
        assert model.destination_arn == model_artifact_obj1.artifact_arn
        assert model.destination_type == "Context"


def test_endpoint_contexts(
    static_dataset_artifact,
    sagemaker_session,
):
    contexts_from_query = static_dataset_artifact.endpoint_contexts()

    associations_from_api = traverse_graph_forward(
        static_dataset_artifact.artifact_arn, sagemaker_session=sagemaker_session
    )

    assert len(contexts_from_query) > 0
    for context in contexts_from_query:
        # assert that the contexts from the query
        # appear in the association list from the lineage API
        assert any(
            x
            for x in associations_from_api
            if x["DestinationArn"] == context.context_arn and x["DestinationType"] == "Endpoint"
        )
