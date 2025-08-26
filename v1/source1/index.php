<?php
// API Configuration
define('API_VERSION', '1.0.0');
define('API_NAME', 'TINSIG Illegal Mining API');
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

// Illegal mining data
$illegalMiningData = [
    [
        'id' => 'FIM/01/25/00001',
        'mobile_id' => 'FIM1735790356829',
        'kabupaten' => 'Bangka Selatan',
        'tanggal_survey' => '2025-01-02',
        'latitude' => -3.028195,
        'longitude' => 106.4837467,
        'nama_pemilik' => 'Amri',
        'jenis_tambang' => 'TAMBANG BESAR ILEGAL',
        'kecamatan' => 'Toboali',
        'jumlah_pekerja' => 2,
        'estimasi_produksi_hari' => 30
    ],
    [
        'id' => 'FIM/01/25/00002',
        'mobile_id' => 'FIM1736133665771',
        'kabupaten' => 'Bangka Selatan',
        'tanggal_survey' => '2025-01-06',
        'latitude' => -2.9378167,
        'longitude' => 106.4983867,
        'nama_pemilik' => 'aden,pian,jek',
        'jenis_tambang' => 'TAMBANG KECIL ILEGAL',
        'kecamatan' => 'Toboali',
        'jumlah_pekerja' => 3,
        'estimasi_produksi_hari' => 5
    ],
    [
        'id' => 'FIM/01/25/00003',
        'mobile_id' => 'FIM1736413003048',
        'kabupaten' => 'Bangka Selatan',
        'tanggal_survey' => '2025-01-09',
        'latitude' => -3.0268233,
        'longitude' => 106.5027317,
        'nama_pemilik' => 'Hen ojek',
        'jenis_tambang' => 'TAMBANG SEMPROT ILEGAL',
        'kecamatan' => 'Toboali',
        'jumlah_pekerja' => 3,
        'estimasi_produksi_hari' => 20
    ],
    [
        'id' => 'FIM/01/25/00004',
        'mobile_id' => 'FIM1736753958170',
        'kabupaten' => 'Bangka Selatan',
        'tanggal_survey' => '2025-01-13',
        'latitude' => -3.0290933,
        'longitude' => 106.516585,
        'nama_pemilik' => 'monok',
        'jenis_tambang' => 'TAMBANG SEMPROT ILEGAL',
        'kecamatan' => 'Toboali',
        'jumlah_pekerja' => 4,
        'estimasi_produksi_hari' => 5
    ],
    [
        'id' => 'FIM/01/25/00005',
        'mobile_id' => 'FIM1736756257211',
        'kabupaten' => 'Bangka Selatan',
        'tanggal_survey' => '2025-01-13',
        'latitude' => -3.0280399,
        'longitude' => 106.5103133,
        'nama_pemilik' => 'Dedi',
        'jenis_tambang' => 'TAMBANG MANUAL ILEGAL',
        'kecamatan' => 'Toboali',
        'jumlah_pekerja' => 9,
        'estimasi_produksi_hari' => 9
    ]
];

// Apply filters
$filteredData = $illegalMiningData;
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
echo successResponse($result, 'Illegal mining data retrieved successfully');
?>
