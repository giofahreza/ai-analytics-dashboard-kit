<?php
// API Configuration
define('API_VERSION', '1.0.0');
define('API_NAME', 'TINSIG Production API');
define('DEFAULT_LIMIT', 100);
define('MAX_LIMIT', 1000);

// Set headers
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Helper functions
function successResponse($data, $message = 'Success') {
    return json_encode([
        'status' => 'success',
        'message' => $message,
        'timestamp' => date('Y-m-d H:i:s'),
        'data' => $data
    ], JSON_PRETTY_PRINT);
}

function paginate($data, $page = 1, $limit = 100) {
    $total = count($data);
    $totalPages = ceil($total / $limit);
    $offset = ($page - 1) * $limit;
    $paginatedData = array_slice($data, $offset, $limit);
    
    return [
        'data' => $paginatedData,
        'pagination' => [
            'current_page' => (int)$page,
            'per_page' => (int)$limit,
            'total_records' => $total,
            'total_pages' => $totalPages
        ]
    ];
}

// Get parameters
$params = array_merge($_GET, $_POST);
$page = isset($params['page']) ? (int)$params['page'] : 1;
$limit = isset($params['limit']) ? min((int)$params['limit'], MAX_LIMIT) : DEFAULT_LIMIT;

// Production data
$productionData = [
    [
        'id' => 'PBT001',
        'tanggal_produksi' => '2025-01-15',
        'lokasi' => 'DU 1541 B',
        'kabupaten' => 'Bangka Selatan',
        'kecamatan' => 'Toboali',
        'produksi_ton' => 25.5,
        'kadar_sn' => 68.5,
        'metode_tambang' => 'Open Pit',
        'operator' => 'PT Timah Tbk',
        'latitude' => -3.028195,
        'longitude' => 106.483747
    ],
    [
        'id' => 'PBT002',
        'tanggal_produksi' => '2025-01-16',
        'lokasi' => 'DU 1548',
        'kabupaten' => 'Bangka',
        'kecamatan' => 'Sungailiat',
        'produksi_ton' => 32.8,
        'kadar_sn' => 71.2,
        'metode_tambang' => 'Marine Dredging',
        'operator' => 'PT Timah Tbk',
        'latitude' => -1.8144,
        'longitude' => 106.1932
    ],
    [
        'id' => 'PBT003',
        'tanggal_produksi' => '2025-01-17',
        'lokasi' => 'DU 1555',
        'kabupaten' => 'Bangka',
        'kecamatan' => 'Sungailiat',
        'produksi_ton' => 18.3,
        'kadar_sn' => 65.8,
        'metode_tambang' => 'Marine Dredging',
        'operator' => 'PT Timah Tbk',
        'latitude' => -1.6399,
        'longitude' => 106.0493
    ],
    [
        'id' => 'PBT004',
        'tanggal_produksi' => '2025-01-18',
        'lokasi' => 'DU 1559',
        'kabupaten' => 'Bangka',
        'kecamatan' => 'Belinyu',
        'produksi_ton' => 22.7,
        'kadar_sn' => 69.1,
        'metode_tambang' => 'Marine Dredging',
        'operator' => 'PT Timah Tbk',
        'latitude' => -1.8061,
        'longitude' => 105.7806
    ],
    [
        'id' => 'PBT005',
        'tanggal_produksi' => '2025-01-19',
        'lokasi' => 'DU 1551',
        'kabupaten' => 'Bangka',
        'kecamatan' => 'Jebus',
        'produksi_ton' => 15.9,
        'kadar_sn' => 72.3,
        'metode_tambang' => 'Marine Dredging',
        'operator' => 'PT Timah Tbk',
        'latitude' => -1.6499,
        'longitude' => 105.7188
    ]
];

// Apply filters
$filteredData = $productionData;
if (isset($params['kabupaten'])) {
    $filteredData = array_filter($filteredData, function($item) use ($params) {
        return stripos($item['kabupaten'], $params['kabupaten']) !== false;
    });
}
if (isset($params['kecamatan'])) {
    $filteredData = array_filter($filteredData, function($item) use ($params) {
        return stripos($item['kecamatan'], $params['kecamatan']) !== false;
    });
}

$result = paginate(array_values($filteredData), $page, $limit);
echo successResponse($result, 'Tin ore production data retrieved successfully');
?>
