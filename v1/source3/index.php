<?php
// API Configuration
define('API_VERSION', '1.0.0');
define('API_NAME', 'TINSIG IUP API');
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

// IUP data
$iupData = [
    [
        'name' => '1548',
        'du' => '1548',
        'longitude' => 106.1932,
        'latitude' => -1.8144,
        'daerah' => 'Lt. A. Kantung - Sungailiat',
        'luas' => 9919.00,
        'no_sk' => '188.45/462/Tamben/2010',
        'tgl_sk' => '27 Apr 2010',
        'cnc' => 'II',
        'status' => 'Active'
    ],
    [
        'name' => '1555',
        'du' => '1555',
        'longitude' => 106.0493,
        'latitude' => -1.6399,
        'daerah' => 'Lt. Deniang - Sungailiat',
        'luas' => 6839.00,
        'no_sk' => '188.45/463/Tamben/2010',
        'tgl_sk' => '27 Apr 2010',
        'cnc' => 'II',
        'status' => 'Active'
    ],
    [
        'name' => '1559',
        'du' => '1559',
        'longitude' => 105.7806,
        'latitude' => -1.8061,
        'daerah' => 'Lt. P. Danta - Belinyu',
        'luas' => 1839.00,
        'no_sk' => '188.45/464/Tamben/2010',
        'tgl_sk' => '27 Apr 2010',
        'cnc' => 'II',
        'status' => 'Active'
    ],
    [
        'name' => '1551',
        'du' => '1551',
        'longitude' => 105.7188,
        'latitude' => -1.6499,
        'daerah' => 'Lt. Bakit - Jebus',
        'luas' => 1461.00,
        'no_sk' => '188.45/098/2.03.02/2010',
        'tgl_sk' => '28 April 2010',
        'cnc' => 'III',
        'status' => 'Active'
    ],
    [
        'name' => '1549',
        'du' => '1549',
        'longitude' => 105.3920,
        'latitude' => -1.5792,
        'daerah' => 'Lt. Kebiang/Penganak - Jebus',
        'luas' => 15050.00,
        'no_sk' => '188.45/097/2.03.02/2010',
        'tgl_sk' => '28 April 2010',
        'cnc' => 'III',
        'status' => 'Active'
    ],
    [
        'name' => '1545',
        'du' => '1545',
        'longitude' => 105.6401,
        'latitude' => -2.1202,
        'daerah' => 'Lt. Tempilang - Kelapa',
        'luas' => 5383.49,
        'no_sk' => '188.45/096/2.03.02/2010',
        'tgl_sk' => '28 April 2010',
        'cnc' => 'III',
        'status' => 'Active'
    ]
];

// Apply filters
$filteredData = $iupData;
if (isset($params['daerah'])) {
    $filteredData = array_filter($filteredData, function($item) use ($params) {
        return stripos($item['daerah'], $params['daerah']) !== false;
    });
}
if (isset($params['status'])) {
    $filteredData = array_filter($filteredData, function($item) use ($params) {
        return stripos($item['status'], $params['status']) !== false;
    });
}

$result = paginate(array_values($filteredData), $page, $limit);
echo successResponse($result, 'Marine IUP data retrieved successfully');
?>
