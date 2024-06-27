from dotenv import load_dotenv
import mlflow
from mlops.utils.settings import MLFLOW_TRACKING_URI

load_dotenv()


class ModelPromotion:
    """
    Promote model by adding alias -> Default: candidate
    and tag -> Default: validation_status=pending
    """
    def __init__(self,
                 model_name: str,
                 mlflow_tracking_uri: str = MLFLOW_TRACKING_URI):
        self.model_name = model_name

        # you can set your tracking server URI programmatically:
        mlflow.set_tracking_uri(mlflow_tracking_uri)

        self.client = mlflow.MlflowClient()

    def promote_model(self, version: str, alias: str = 'candidate', tag: str = 'validation_status', tag_value: str = 'pending') -> None:
        """
        Promoted model by adding alias -> Default: candidate
        and tag -> Default: validation_status=pending

        :param version: version of the model to promote
        :param alias: alias of the model
        :param tag: tag to add to the model
        :param tag_value: value of the tag to add to the model
        :return: None
        :example:
            >>> promotion = ModelPromotion(model_name='diamond_model')
            >>> promotion.promote_model(version='1')
            >>> promotion.promote_model(version='1', alias='candidate')
            >>> promotion.promote_model(version='1', alias='candidate', tag='validation_status=pending')
            >>> promotion.promote_model(version='1', alias='candidate', tag='validation_status=pending')
            >>> promotion.promote_model(version='1', alias='candidate', tag='validation_status=pending')
            >>> promotion.promote_model(version='1', alias='candidate', tag='validation_status=pending')
            >>> promotion.promote_model(version='1', alias='candidate', tag='validation_status=pending')
        """

        self.assign_alias_to_model(version=version, alias=alias)
        self.assign_tag_to_model(version=version, tag=tag, tag_value=tag_value)

    def assign_alias_to_model(self, version, alias: str) -> None:
        """
        Assign alias to model

        :param version: version of the model to assign alias
        :param alias: alias of the model
        :return: None
        :example:
            >>> promotion = ModelPromotion(model_name='diamond_model')
            >>> promotion.assign_alias_to_model(version='1', alias='candidate')
        """

        self.client.set_registered_model_alias(name=self.model_name, alias=alias, version=version)

    def assign_tag_to_model(self, version: str, tag: str, tag_value: str) -> None:
        """
        Assign tag to model

        :param version: version of the model
        :param alias: alias of the model
        :return: None
        :example:
            >>> promotion = ModelPromotion(model_name='diamond_model')
            >>> promotion.assign_tag_to_model(version='1', tag='validation_status, tag_value='pending')
        """

        self.client.set_model_version_tag(name=self.model_name, version=version, key=tag,
                                          value=tag_value)
