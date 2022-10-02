class Environment():

    # * token para emitir boleta factura electronica
    # url_oea = 'http://192.168.100.3:8000/api/'
    url_oea = 'https://app.oea.edu.pe/api/'
    url_sunat = 'https://facturacion.apisperu.com/api/v1/invoice/'
    # ? prueba
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2NTcxNjA5MjQsImV4cCI6NDgxMDc2MDkyNCwidXNlcm5hbWUiOiJtYW51ZWxqZWluZXIiLCJjb21wYW55IjoiMjA2MDI3NzU2ODAifQ.ZKdjYUYhiQgKirHO_jBRZcPlO2x33Pdqs2lW2KgNyIB0TWvEQrUY1W7J28f6yKrQEjGkVaClJQwFYzpWymp2U5ufA2mJQ9eY5J1E5HIUMBI6qXtwf_sJDRXWFCgIwy-4GSvlisbDF-YdYKnr4YGMaolrdyvsZkP-7-5Q8zOMhtkERCtsNdsl0BBmEc_4w7ZeSaiRCSbv6DZwcXkxgrtOrNxaMVnzDVubvoLJuJ27cUk6jvrqlABpJp-irKMwB0U64Dx2Y3Fzgs743WYf2dTz83x_-JCMaNB24CVz-3DhRrWGAFaFyFm5H4lKRtPSNqm-ZeHZ5ZGmBIWvBJXGuRSXmJuivZmIOxm-bIB2XfDM3CC3LQkuIV5OIW2s5kOXAv-44icVv03M-dmROObGQcT4daX_F2sp4aBk6L71UtMwtMYMHZycCajUkj3W5UP88QuBUZmwEaQ7iVxtpu1tk8T0z_RLl0nhWKJM04idXmTwZoaO595CDrJCa5VHT68RLLK1nspi63SuAcuE6z81dEIxFC6BHbReb5uT1-BiyuLV76r6BE7S2HguZdcvT75JNHaf7zrO7enw76EjlGkNDziBS6qp9eLO7ohLR5Ffq23Dd6DnPPzW-qnsnjlAukcV280qwGnOFkW1Zd9imSYwHHr3MNCQVo-U9wLm-_Y90HswLdw'
    # ? produccion
    # token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2NTAzMDI0NDgsImV4cCI6NDgwMzkwMjQ0OCwidXNlcm5hbWUiOiJPRUFFZHVjYWNpb24iLCJjb21wYW55IjoiMjA1NDUyODA2MDUifQ.M2V7hJX31eBGcZF6uH8o3xalD6zSUMheoCm0SEDG9T-jNVVJ0Plb1pZH2pou-0GbLk1z38ssGwMOC5oZh_0Hv3jC12qnFaLDOBsUdPBk6PlGCc2pF2Ej6pKo7tqJp2r5JNC6EyJIJxwtNFWjQGIegIM8bBkLzOKH1lUyWX15yvB33Fd5oA0WWOXMPLa-FT5kLaQ70IVhPAliVskfb84gQUJ6hxmZ5C7cq4fe8bRIeW8veijOM9YeOli0gnObNZ3zzbSJRotdOdiIydMTpFxMHyX6IPLmrFZGsrDmgSS6SfRRMD36it11BI0p28CKFT90oZmi9E3XVYKBLDLwKGOv0vQMo-U2sQkB-Qb97Vy2-Jcaf1l5M0csG6eBR6NrjhIy_97WShha6FXTjd6325J9ImGnNeMvLbzLgj7ZYOTG4T5Dgp_tPk6Ty3gqD7wEwGh2oyJWWu9Q57pdhmyKu8m8MQaFlkVfYgb1TwG1uTic1pmT13g0WMuGkai9XIgUgG9OFPBGQcsoHXXlj7f-OC3MAektDLlOMfH7yXBq5Tqae09cms-VBFY846E4jqXh9_X2tqqwPKkpv2gQEUWfLVaVlpjntmn33ZvNNoSvYnWGfDjV-LaA3D8Mf1Y91HAQycJ-MOIVZqgKVmrj-PWpqdV7rf5oItTL50HidI7FFqKzm8k'
    # * ultima version de la api de facturacion
    ublVersion = '2.1'

    COMPANY_RUC=20602775680
    COMPANY_RZSOCIAL= "JATCONSULTING S.A.C"
    COMAPANY_N_COMERCIAL= "JATCONSULTING"
    COMAPANY_ADDRESS= "CALLE SAN INGNACIO CALLO CUADRA 13 L1"
    COMAPANY_DEPARTAMENTO= "OEA LIMA"
    COMAPANY_PROVINCIA= "OEA LIMA"
    COMAPANY_DISTRITO= "OEA SAN MIGUEL"
    COMAPANY_UBIGEO= "150101"

    def __init__(self) -> None:
        return
    
    def get_ubl_version(self) -> str:
        return self.ublVersion
    
    def get_url_sunat(self) -> str:
        return self.url_sunat
    
    def get_token(self) -> str:
        return self.token

    def get_company(self) -> dict:
        company : dict = {
                "ruc": self.COMPANY_RUC,
                "razonSocial": self.COMPANY_RZSOCIAL,
                "nombreComercial": self.COMAPANY_N_COMERCIAL,
                "address": {
                    "direccion": self.COMAPANY_ADDRESS,
                    "provincia": self.COMAPANY_DEPARTAMENTO,
                    "departamento": self.COMAPANY_PROVINCIA,
                    "distrito": self.COMAPANY_DISTRITO,
                    "ubigueo": self.COMAPANY_UBIGEO
                }
            }
        return company