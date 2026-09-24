// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.20;

/// @title  SavitsAssetRegistry (SAR)
/// @notice Registro on-chain de ativos científicos (conjuntos de dados, modelos),
///         suas versões, eventos de proveniência, certificações e consentimentos.
/// @dev    PROTÓTIPO EXPERIMENTAL — Projeto SAVITS / IBICT, frente Blockchain-RBB.
///
///         PRINCÍPIO DE PROJETO (LGPD): este contrato NÃO armazena dado pessoal,
///         conteúdo de artefato, metadado descritivo nem URL. Armazena apenas
///         resumos criptográficos, referências pseudonimizadas, carimbos de tempo
///         e endereços de remetente. A localização e a descrição do objeto
///         permanecem off-chain (dARK/PID e repositório institucional).
contract SavitsAssetRegistry {
    // ------------------------------------------------------------------ papéis
    uint8 public constant ROLE_ADMIN = 1; // 0001
    uint8 public constant ROLE_REGISTRAR = 2; // 0010
    uint8 public constant ROLE_CERTIFIER = 4; // 0100
    uint8 public constant ROLE_CONSENT = 8; // 1000

    mapping(address => uint8) public roles;

    modifier only(uint8 r) {
        require(roles[msg.sender] & r != 0, "SAR: sem permissao");
        _;
    }

    // ------------------------------------------------------------------ tipos
    enum AssetKind {
        DATASET,
        MODEL,
        PIPELINE,
        RESULT,
        DOCUMENT,
        OTHER
    }

    enum EventType {
        CREATED,
        INGESTED,
        PROCESSED,
        TRAINED,
        EVALUATED,
        DERIVED,
        PUBLISHED,
        DEPRECATED,
        OTHER
    }

    enum CertStatus {
        NONE,
        ACTIVE,
        REVOKED
    }

    struct Asset {
        bool exists;
        AssetKind kind;
        address registrar;
        uint64 createdAt;
        string pid; // identificador persistente externo (ARK/dARK); pode ser vazio
    }

    struct Version {
        bytes32 contentHash; // resumo do artefato (algoritmo em hashAlgo)
        bytes8 hashAlgo; // rótulo do algoritmo, ex.: "sha2-256"
        bytes32 metadataHash; // resumo do registro de metadados off-chain
        uint64 timestamp;
        address registrar;
    }

    struct ProvEvent {
        bytes32 assetId;
        uint32 versionIndex;
        EventType eventType;
        bytes32 payloadHash; // resumo do registro detalhado off-chain
        bytes32[] parents; // referências de versão de origem (versionRef)
        uint64 timestamp;
        address actor;
    }

    struct Certification {
        bytes32 versionRefId;
        address certifier;
        bytes32 statementHash; // resumo do documento de certificação off-chain
        uint64 issuedAt;
        uint64 revokedAt;
        CertStatus status;
    }

    struct Consent {
        bool exists;
        bytes32 subjectRef; // pseudônimo derivado off-chain (HMAC com chave custodiada)
        bytes32 termsHash; // resumo do termo de consentimento
        bytes32 scopeHash; // resumo da finalidade/escopo autorizado
        uint64 grantedAt;
        uint64 revokedAt;
        address recorder;
    }

    // ------------------------------------------------------------- armazenamento
    mapping(bytes32 => Asset) private _assets;
    mapping(bytes32 => Version[]) private _versions;
    mapping(bytes32 => uint256) private _hashIndex; // keccak(assetId,contentHash) => idx+1
    mapping(bytes32 => uint256[]) private _certsOfVersion;
    mapping(bytes32 => Consent) private _consents;

    ProvEvent[] private _events;
    Certification[] private _certs;

    bytes32[] private _assetIds;

    // ------------------------------------------------------------------ eventos
    event AssetRegistered(bytes32 indexed assetId, AssetKind kind, address indexed registrar, uint64 timestamp);
    event PidBound(bytes32 indexed assetId, string pid, address indexed actor, uint64 timestamp);
    event VersionRegistered(
        bytes32 indexed assetId,
        uint32 indexed versionIndex,
        bytes32 indexed contentHash,
        bytes8 hashAlgo,
        uint64 timestamp
    );
    event ProvenanceRecorded(
        uint256 indexed eventId, bytes32 indexed assetId, uint32 versionIndex, EventType eventType, uint64 timestamp
    );
    event Certified(uint256 indexed certId, bytes32 indexed versionRefId, address indexed certifier, uint64 timestamp);
    event CertificationRevoked(uint256 indexed certId, bytes32 reasonHash, uint64 timestamp);
    event ConsentRegistered(bytes32 indexed consentId, bytes32 indexed subjectRef, bytes32 scopeHash, uint64 timestamp);
    event ConsentRevoked(bytes32 indexed consentId, bytes32 reasonHash, uint64 timestamp);
    event RoleSet(address indexed account, uint8 roles);

    // ---------------------------------------------------------------- construtor
    constructor() {
        roles[msg.sender] = ROLE_ADMIN | ROLE_REGISTRAR | ROLE_CERTIFIER | ROLE_CONSENT;
        emit RoleSet(msg.sender, roles[msg.sender]);
    }

    function setRole(address account, uint8 r) external only(ROLE_ADMIN) {
        roles[account] = r;
        emit RoleSet(account, r);
    }

    // ------------------------------------------------------------------ helpers
    /// @notice Referência canônica de uma versão: keccak256(assetId, versionIndex).
    function versionRef(bytes32 assetId, uint32 versionIndex) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(assetId, versionIndex));
    }

    function _now() internal view returns (uint64) {
        return uint64(block.timestamp);
    }

    // ------------------------------------------------------------------- ativos
    function registerAsset(bytes32 assetId, AssetKind kind, string calldata pid) external only(ROLE_REGISTRAR) {
        require(assetId != bytes32(0), "SAR: assetId nulo");
        require(!_assets[assetId].exists, "SAR: ativo ja registrado");
        _assets[assetId] =
            Asset({exists: true, kind: kind, registrar: msg.sender, createdAt: _now(), pid: pid});
        _assetIds.push(assetId);
        emit AssetRegistered(assetId, kind, msg.sender, _now());
        if (bytes(pid).length > 0) emit PidBound(assetId, pid, msg.sender, _now());
    }

    /// @notice Vincula (ou substitui) o PID externo de um ativo.
    /// @dev    O PID é cunhado fora deste contrato (dARK). Aqui é apenas referência.
    function bindPid(bytes32 assetId, string calldata pid) external only(ROLE_REGISTRAR) {
        require(_assets[assetId].exists, "SAR: ativo inexistente");
        require(bytes(pid).length > 0, "SAR: pid vazio");
        _assets[assetId].pid = pid;
        emit PidBound(assetId, pid, msg.sender, _now());
    }

    // ------------------------------------------------------------------ versoes
    function registerVersion(bytes32 assetId, bytes32 contentHash, bytes8 hashAlgo, bytes32 metadataHash)
        external
        only(ROLE_REGISTRAR)
        returns (uint32 versionIndex)
    {
        require(_assets[assetId].exists, "SAR: ativo inexistente");
        require(contentHash != bytes32(0), "SAR: hash nulo");
        bytes32 k = keccak256(abi.encodePacked(assetId, contentHash));
        require(_hashIndex[k] == 0, "SAR: conteudo ja registrado");

        _versions[assetId].push(
            Version({
                contentHash: contentHash,
                hashAlgo: hashAlgo,
                metadataHash: metadataHash,
                timestamp: _now(),
                registrar: msg.sender
            })
        );
        versionIndex = uint32(_versions[assetId].length - 1);
        _hashIndex[k] = uint256(versionIndex) + 1;
        emit VersionRegistered(assetId, versionIndex, contentHash, hashAlgo, _now());
    }

    // -------------------------------------------------------------- proveniencia
    function registerEvent(
        bytes32 assetId,
        uint32 versionIndex,
        EventType eventType,
        bytes32 payloadHash,
        bytes32[] calldata parents
    ) external only(ROLE_REGISTRAR) returns (uint256 eventId) {
        require(_assets[assetId].exists, "SAR: ativo inexistente");
        require(versionIndex < _versions[assetId].length, "SAR: versao inexistente");
        _events.push(
            ProvEvent({
                assetId: assetId,
                versionIndex: versionIndex,
                eventType: eventType,
                payloadHash: payloadHash,
                parents: parents,
                timestamp: _now(),
                actor: msg.sender
            })
        );
        eventId = _events.length - 1;
        emit ProvenanceRecorded(eventId, assetId, versionIndex, eventType, _now());
    }

    // -------------------------------------------------------------- certificacao
    function certify(bytes32 versionRefId, bytes32 statementHash)
        external
        only(ROLE_CERTIFIER)
        returns (uint256 certId)
    {
        require(versionRefId != bytes32(0), "SAR: ref nula");
        _certs.push(
            Certification({
                versionRefId: versionRefId,
                certifier: msg.sender,
                statementHash: statementHash,
                issuedAt: _now(),
                revokedAt: 0,
                status: CertStatus.ACTIVE
            })
        );
        certId = _certs.length - 1;
        _certsOfVersion[versionRefId].push(certId);
        emit Certified(certId, versionRefId, msg.sender, _now());
    }

    function revokeCertification(uint256 certId, bytes32 reasonHash) external only(ROLE_CERTIFIER) {
        require(certId < _certs.length, "SAR: certificado inexistente");
        Certification storage c = _certs[certId];
        require(c.status == CertStatus.ACTIVE, "SAR: certificado nao ativo");
        require(c.certifier == msg.sender, "SAR: apenas o emissor revoga");
        c.status = CertStatus.REVOKED;
        c.revokedAt = _now();
        emit CertificationRevoked(certId, reasonHash, _now());
    }

    // ------------------------------------------------------------- consentimento
    function registerConsent(bytes32 consentId, bytes32 subjectRef, bytes32 termsHash, bytes32 scopeHash)
        external
        only(ROLE_CONSENT)
    {
        require(!_consents[consentId].exists, "SAR: consentimento ja registrado");
        _consents[consentId] = Consent({
            exists: true,
            subjectRef: subjectRef,
            termsHash: termsHash,
            scopeHash: scopeHash,
            grantedAt: _now(),
            revokedAt: 0,
            recorder: msg.sender
        });
        emit ConsentRegistered(consentId, subjectRef, scopeHash, _now());
    }

    function revokeConsent(bytes32 consentId, bytes32 reasonHash) external only(ROLE_CONSENT) {
        Consent storage c = _consents[consentId];
        require(c.exists, "SAR: consentimento inexistente");
        require(c.revokedAt == 0, "SAR: ja revogado");
        c.revokedAt = _now();
        emit ConsentRevoked(consentId, reasonHash, _now());
    }

    function isConsentActive(bytes32 consentId) external view returns (bool) {
        Consent storage c = _consents[consentId];
        return c.exists && c.revokedAt == 0;
    }

    // --------------------------------------------------------------- consultas
    function getAsset(bytes32 assetId)
        external
        view
        returns (bool exists, AssetKind kind, address registrar, uint64 createdAt, string memory pid, uint256 nVersions)
    {
        Asset storage a = _assets[assetId];
        return (a.exists, a.kind, a.registrar, a.createdAt, a.pid, _versions[assetId].length);
    }

    function versionCount(bytes32 assetId) external view returns (uint256) {
        return _versions[assetId].length;
    }

    function getVersion(bytes32 assetId, uint32 index) external view returns (Version memory) {
        require(index < _versions[assetId].length, "SAR: versao inexistente");
        return _versions[assetId][index];
    }

    /// @notice Verifica se um resumo corresponde a alguma versão registrada do ativo.
    /// @return found     verdadeiro se o conteúdo consta do registro
    /// @return index     índice da versão correspondente
    /// @return timestamp carimbo de tempo do registro
    function verifyAsset(bytes32 assetId, bytes32 contentHash)
        external
        view
        returns (bool found, uint32 index, uint64 timestamp)
    {
        uint256 i = _hashIndex[keccak256(abi.encodePacked(assetId, contentHash))];
        if (i == 0) return (false, 0, 0);
        index = uint32(i - 1);
        return (true, index, _versions[assetId][index].timestamp);
    }

    function eventCount() external view returns (uint256) {
        return _events.length;
    }

    function getEvent(uint256 eventId) external view returns (ProvEvent memory) {
        require(eventId < _events.length, "SAR: evento inexistente");
        return _events[eventId];
    }

    function certificationsOf(bytes32 versionRefId) external view returns (uint256[] memory) {
        return _certsOfVersion[versionRefId];
    }

    function getCertification(uint256 certId) external view returns (Certification memory) {
        require(certId < _certs.length, "SAR: certificado inexistente");
        return _certs[certId];
    }

    function getConsent(bytes32 consentId) external view returns (Consent memory) {
        return _consents[consentId];
    }

    function assetCount() external view returns (uint256) {
        return _assetIds.length;
    }
}
