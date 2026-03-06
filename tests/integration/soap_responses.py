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
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Header/>
    <soap:Body>
        <FECAESolicitarResponse xmlns="http://ar.gov.afip.dif.FEV1/">
            <FECAESolicitarResult>
                <FeCabResp>
                    <Cuit>30740253022</Cuit>
                    <PtoVta>1</PtoVta>
                    <CbteTipo>6</CbteTipo>
                    <FchProceso>20251226123045</FchProceso>
                    <CantReg>1</CantReg>
                    <Resultado>A</Resultado>
                    <Reproceso>N</Reproceso>
                </FeCabResp>
                <FeDetResp>
                    <FECAEDetResponse>
                        <Concepto>1</Concepto>
                        <DocTipo>99</DocTipo>
                        <DocNro>0</DocNro>
                        <CbteDesde>2</CbteDesde>
                        <CbteHasta>2</CbteHasta>
                        <CbteFch>20260224</CbteFch>
                        <Resultado>A</Resultado>
                        <CAE>80050022488317</CAE>
                        <CAEFchVto>20260306</CAEFchVto>
                    </FECAEDetResponse>
                </FeDetResp>
            </FECAESolicitarResult>
        </FECAESolicitarResponse>
    </soap:Body>
</soap:Envelope>
"""

FECompTotXRequestResponse = """<?xml version="1.0" encoding="utf-8"?>
<soap-env:Envelope
    xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:ar="http://ar.gov.afip.dif.FEV1/">
    <soap-env:Header/>
    <soap-env:Body>
        <FECompTotXRequestResponse>
            <FECompTotXRequestResult>
                <RegXReq>1</RegXReq>
            </FECompTotXRequestResult>
        </FECompTotXRequestResponse>
    </soap-env:Body>
</soap-env:Envelope>
"""

FeCompUltimoAutorizadoResponse = """<?xml version="1.0" encoding="utf-8"?>
<soap-env:Envelope
    xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:ar="http://ar.gov.afip.dif.FEV1/">
    <soap-env:Header/>
    <soap-env:Body>
        <FECompUltimoAutorizadoResponse>
            <FECompUltimoAutorizadoResult>
                <PtoVta>1</PtoVta>
                <CbteTipo>6</CbteTipo>
                <CbteNro>1548</CbteNro>
            </FECompUltimoAutorizadoResult>
        </FECompUltimoAutorizadoResponse>
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
                <DocTipo>96</DocTipo>
                <DocNro>12345678</DocNro>
                <CbteDesde>100</CbteDesde>
                <CbteHasta>100</CbteHasta>
                <CbteFch>20251226</CbteFch>
                <ImpTotal>1210</ImpTotal>
                <ImpTotConc>0</ImpTotConc>
                <ImpNeto>1000</ImpNeto>
                <ImpOpEx>0</ImpOpEx>
                <ImpTrib>0</ImpTrib>
                <ImpIVA>210</ImpIVA>
                <FchServDesde/>
                <FchServHasta/>
                <FchVtoPago/>
                <MonId>PES</MonId>
                <MonCotiz>1</MonCotiz>
                <CondicionIVAReceptorId>5</CondicionIVAReceptorId>
                <Iva>
                    <AlicIva>
                    <Id>5</Id>
                    <BaseImp>1000</BaseImp>
                    <Importe>210</Importe>
                    </AlicIva>
                </Iva>
                <Resultado>A</Resultado>
                <CodAutorizacion>75522302377893</CodAutorizacion>
                <EmisionTipo>CAE</EmisionTipo>
                <FchVto>20260105</FchVto>
                <FchProceso>20251226010205</FchProceso>
                <PtoVta>1</PtoVta>
                <CbteTipo>6</CbteTipo>
            </ResultGet>
            </FECompConsultarResult>
        </FECompConsultarResponse>
    </soap:Body>
</soap:Envelope>
"""

FECAEARegInformativoResponse = """<?xml version="1.0" encoding="utf-8"?>
<soap-env:Envelope
    xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:ar="http://ar.gov.afip.dif.FEV1/">
    <soap-env:Header/>
    <soap-env:Body>
        <FECAEARegInformativoResponse>
            <FECAEARegInformativoResult>
                <FeCabResp>
                    <Cuit>30740253022</Cuit>
                    <PtoVta>1</PtoVta>
                    <CbteTipo>1</CbteTipo> 
                    <FchProceso>20260221101530</FchProceso>
                    <CantReg>1</CantReg>
                    <Resultado>A</Resultado> 
                </FeCabResp>
                <FeDetResp>
                    <FECAEADetResponse>
                        <Concepto>1</Concepto> 
                        <DocTipo>80</DocTipo> 
                        <DocNro>20123456789</DocNro>
                        <CbteDesde>1</CbteDesde>
                        <CbteHasta>1</CbteHasta>
                        <CbteFch>20260224</CbteFch>
                        <Resultado>A</Resultado>
                        <CAEA>26081234567890</CAEA> 
                    </FECAEADetResponse>
                </FeDetResp>
            </FECAEARegInformativoResult>
        </FECAEARegInformativoResponse>
    </soap-env:Body>
</soap-env:Envelope>
"""

FECAEASolicitarResponse = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope 
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <soap:Body>
        <FECAEASolicitarResponse xmlns="http://ar.gov.afip.dif.FEV1/">
            <FECAEASolicitarResult>
                <ResultGet>
                    <CAEA>87080030400901</CAEA> 
                    <Periodo>202602</Periodo>
                    <Orden>2</Orden>
                    <FchVigDesde>20260216</FchVigDesde>
                    <FchVigHasta>20260228</FchVigHasta>
                    <FchProceso>20260222223015</FchProceso>
                </ResultGet>
            </FECAEASolicitarResult>
        </FECAEASolicitarResponse>
    </soap:Body>
</soap:Envelope>
"""

FECAEASinMovimientoConsultarResponse = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope 
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <soap:Body>
        <FECAEASinMovimientoConsultarResponse xmlns="http://ar.gov.afip.dif.FEV1/">
            <FECAEASinMovimientoConsultarResult>
                <ResultGet>
                    <FECAEASinMov>
                        <CAEA>87080030400901</CAEA>
                        <PtoVta>1</PtoVta>
                        <FchProceso>20260224</FchProceso>
                    </FECAEASinMov>
                </ResultGet>
            </FECAEASinMovimientoConsultarResult>
        </FECAEASinMovimientoConsultarResponse>
    </soap:Body>
</soap:Envelope>
"""

