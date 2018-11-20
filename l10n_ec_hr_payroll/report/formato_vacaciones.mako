<html>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<head>
    <style type="text/css">
    table { page-break-inside:auto }
    tr    { page-break-inside:avoid; page-break-after:auto }
    thead { display:table-header-group }
    tfoot { display:table-footer-group }
    </style>
</head>
<body>
    %for holidays in objects:
    <table  cellspacing=0 width="100%">
    	<tr>
    	<td width="100%" colspan="2" style="text-align:center;font-size:18px"><center><b>SOLICITUD APROBACION Y ACEPTACION DE VACACIONES</b></center></td>
    	</tr>
    	<tr>
    	<th width="25%" style="text-align:right;font-size:12px"><b>Cedula:</b></th>
    	<td width="75%" style="text-align:left;font-size:12px">${holidays.employee_id.name}</td>
    	<tr>
    	<th width="25%" style="text-align:right;font-size:12px"><b>Nombre:</b></th>
    	<td width="75%" style="text-align:left;font-size:12px">${holidays.employee_id.name_related}</td>
    	</tr>
    	<tr>
    	<th width="25%" style="text-align:right;font-size:12px"><b>Empresa:</b></th>
    	<td width="75%" style="text-align:left;font-size:12px">${holidays.employee_id.contract_id.company_id.name}</td>
    	</tr>
    	<tr>
    	<th width="25%" style="text-align:right;font-size:12px"><b>Cargo:</b></th>
    	<td width="75%" style="text-align:left;font-size:12px">${holidays.employee_id.contract_id.job_id.name}</td>
    	</tr>
    	<tr>
    	<th width="25%" style="text-align:right;font-size:12px"><b>Departamento:</b></th>
    	<td width="75%" style="text-align:left;font-size:12px">${holidays.employee_id.contract_id.department_id.name}</td>
    	</tr>
    	<tr></br></tr>
    	<tr>
    	<th width="25%" style="text-align:right;font-size:12px"><b>Solicito:</b></th>
    	<td width="75%" style="text-align:left;font-size:12px">${holidays.number_of_days_temp} días de vacaciones</td>
    	</tr>
    	<tr>
    	<th width="25%" style="text-align:right;font-size:12px"><b>Desde:</b></th>
    	<td width="75%" style="text-align:left;font-size:12px">${holidays.date_from}</td>
    	</tr>
    	<tr>
    	<th width="25%" style="text-align:right;font-size:12px"><b>Hasta:</b></th>
    	<td width="75%" style="text-align:left;font-size:12px">${holidays.date_to}</td>
    	</tr>
    	<tr></br></tr>
    	<tr>
    	<th width="25%" style="text-align:right;font-size:12px"><b>Correspondientes al periodo:</b></th>
    	<td width="75%" style="text-align:left;font-size:12px">${holidays.employee_holidays.date_start} - ${holidays.employee_holidays.date_end}</td>
    	</tr>
    	<tr></br></tr>
    	<tr>
    	<td width="100%" colspan="2" style="text-align:center;font-size:12px"><center><b>DETALLE DE VACACIONES</b></center></td>
    	</tr>
    	<tr></br></tr>
    	  <td width="100%" colspan="2" style="text-align:center;">
		<table  cellspacing=0 width="100%" style="font-size:10px;">
			<tr style="vertical-align:top;">
				<th width="55%" style="text-align:center;">RUBRO</th>
				<th width="15%" style="text-align:center;">TOTAL</th>
				<th width="15%" style="text-align:center;">GOZADAS</th>
				<th width="15%" style="text-align:center;">SOLICITADAS</th>
			</tr>
			<tr style="vertical-align:top;">
				<th width="55%" style="text-align:center;">Total de dias de vacaciones anuales</th>
				<td width="15%" style="text-align:center;">${holidays.employee_holidays.days_normal}</td>
				<td width="15%" style="text-align:center;">${holidays.employee_holidays.days_normal_used}</td>
				<td width="15%" style="text-align:center;"></td>
			</tr>
			<tr style="vertical-align:top;">
				<th width="55%" style="text-align:center;">Total de dias de vacaciones anuales adicionales</th>
				<td width="15%" style="text-align:center;">${holidays.employee_holidays.days_extra}</td>
				<td width="15%" style="text-align:center;">${holidays.employee_holidays.days_extra_used}</td>
				<td width="15%" style="text-align:center;"></td>
			</tr>
		</table>
    	  </td>
    	</tr>
    </table>
  <p style="page-break-after:always"></p>
  %endfor

</body>
</html>
