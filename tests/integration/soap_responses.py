loginCmsResponse = """<?xml version='1.0' encoding='UTF-8'?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://wsaa.view.sua.dvadac.desein.afip.gov">
    <soapenv:Body>
        <ns1:loginCmsResponse>
            <ns1:loginCmsReturn><![CDATA[<?xml version="1.0" encoding="UTF-8"?>
                <loginTicketResponse version="1.0">
                    <header>
                        <source>CN=wsaahomo, O=AFIP, C=AR, SERIALNUMBER=CUIT 33693450239</source>
                        <destination>SERIALNUMBER=CUIT 30740253022, CN=certificadodefinitivo</destination>
                        <uniqueId>3634574819</uniqueId>
                        <generationTime>2026-01-07T02:40:09.235-03:00</generationTime>
                        <expirationTime>2026-01-07T14:40:09.235-03:00</expirationTime>
                    </header>
                    <credentials>
                        <token>fake_token</token>
                        <sign>fake_sign</sign>
                    </credentials>
                </loginTicketResponse>]]>
            </ns1:loginCmsReturn>
        </ns1:loginCmsResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""

FECAESolicitarResponse = """<?xml version="1.0" encoding="utf-8"?>
<soap-env:Envelope
    xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:ar="http://ar.gov.afip.dif.FEV1/">
    <soap-env:Header/>
    <soap-env:Body>
        <ar:FECAESolicitarResponse>
            <ar:FECAESolicitarResult>
                <ar:FeCabResp>
                    <ar:Cuit>30740253022</ar:Cuit>
                    <ar:PtoVta>1</ar:PtoVta>
                    <ar:CbteTipo>6</ar:CbteTipo>
                    <ar:FchProceso>20251226123045</ar:FchProceso>
                    <ar:CantReg>1</ar:CantReg>
                    <ar:Resultado>A</ar:Resultado>
                </ar:FeCabResp>
                <ar:FeDetResp>
                    <ar:FECAEDetResponse>
                        <ar:Concepto>1</ar:Concepto>
                        <ar:DocTipo>99</ar:DocTipo>
                        <ar:DocNro>0</ar:DocNro>
                        <ar:CbteDesde>2</ar:CbteDesde>
                        <ar:CbteHasta>2</ar:CbteHasta>
                        <ar:Resultado>A</ar:Resultado>
                    </ar:FECAEDetResponse>
                </ar:FeDetResp>
            </ar:FECAESolicitarResult>
        </ar:FECAESolicitarResponse>
    </soap-env:Body>
</soap-env:Envelope>
"""

FECompTotXRequestResponse = """<?xml version="1.0" encoding="utf-8"?>
<soap-env:Envelope
    xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:ar="http://ar.gov.afip.dif.FEV1/">
    <soap-env:Header/>
    <soap-env:Body>
        <ar:FECompTotXRequestResponse>
            <FECompTotXRequestResult>
                <RegXReq>1</RegXReq>
            </FECompTotXRequestResult>
        </ar:FECompTotXRequestResponse>
    </soap-env:Body>
</soap-env:Envelope>
"""

FeCompUltimoAutorizadoResponse = """<?xml version="1.0" encoding="utf-8"?>
<soap-env:Envelope
    xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:ar="http://ar.gov.afip.dif.FEV1/">
    <soap-env:Header/>
    <soap-env:Body>
        <ar:FECompUltimoAutorizadoResponse>
            <ar:FECompUltimoAutorizadoResult>
                <ar:PtoVta>1</ar:PtoVta>
                <ar:CbteTipo>6</ar:CbteTipo>
                <ar:CbteNro>1548</ar:CbteNro>
            </ar:FECompUltimoAutorizadoResult>
        </ar:FECompUltimoAutorizadoResponse>
    </soap-env:Body>
</soap-env:Envelope>
"""

FECompConsultarResponse = """<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <FECompConsultarResponse xmlns="http://ar.gov.afip.dif.FEV1/">
            <FECompConsultarResult>
                <ResultGet>
                    <Concepto>1</Concepto>
                    <DocTipo>80</DocTipo>
                    <DocNro>20123456789</DocNro>
                    <CbteDesde>100</CbteDesde>
                    <CbteHasta>100</CbteHasta>
                    <CbteFch>20260109</CbteFch>
                    <ImpTotal>100.00</ImpTotal>
                    <ImpTotConc>0.00</ImpTotConc>
                    <ImpNeto>100.00</ImpNeto>
                    <ImpOpEx>0.00</ImpOpEx>
                    <ImpTrib>0.00</ImpTrib>
                    <ImpIVA>21.00</ImpIVA>
                    <MonId>PES</MonId>
                    <MonCotiz>1.000</MonCotiz>
                    
                    <Resultado>A</Resultado>
                    <CodAutorizacion>74123456789012</CodAutorizacion>
                    <EmisionTipo>CAE</EmisionTipo>
                    <FchVto>20260119</FchVto>
                    <FchProceso>20260109120000</FchProceso>
                    
                    <PtoVta>1</PtoVta>
                    <CbteTipo>6</CbteTipo>
                </ResultGet>
                </FECompConsultarResult>
        </FECompConsultarResponse>
    </soap:Body>
</soap:Envelope>
"""