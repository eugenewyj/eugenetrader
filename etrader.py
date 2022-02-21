from tigeropen.common.consts import Language
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.common.util.signature_utils import read_private_key

import yaml
from tigeropen.trade.trade_client import TradeClient
from tigeropen.tiger_open_config import get_client_config


def get_tiger_client_config(sandbox=False):
    """ 获取老虎开放客户端配置

    Args:
        sandbox: 是否请求 sandbox 环境

    Returns:
        TigerOpenClientConfig（老虎开放客户端配置对象）,例如：


    Raises:
        无
    """
    """
    https://www.itiger.com/openapi/info 开发者信息获取
    """
    client_config = TigerOpenClientConfig(sandbox_debug=sandbox)
    client_config.private_key = read_private_key(
        '~/.ssh/rsa_tiger_private_key.pem')
    client_config.tiger_id = '20151371'
    client_config.account = 'U10031621'
    client_config.language = Language.zh_CN  # 可选，不填默认为英语'
    return client_config


path = 'security.yaml'
with open(path, 'rt') as f:
    config = yaml.safe_load(f.read())

tiger_config = config['tiger']
print(tiger_config)

client_config = get_client_config(
    private_key_path=tiger_config['private_key_path'], tiger_id=tiger_config['tiger_id'], account=tiger_config['account'])
trade_client = TradeClient(client_config)
