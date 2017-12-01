class Config:
    hosts = [{'ip': '10.0.0.6'}]
    setups = [
        {
            'hosts': [('10.0.0.5', '10.0.0.6')],
            'settings': {
                'duration': 10,
                'name': 'Testing 10.6->10.5'
            }
        }
    ]

