// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.20;

/// @title  ProofAnchor
/// @notice Ancoragem em lote de provas de integridade por árvore de Merkle.
/// @dev    PROTÓTIPO EXPERIMENTAL — Projeto SAVITS / IBICT.
///         Uma transação ancora N objetos: publica-se apenas a raiz; cada
///         detentor recebe um caminho de inclusão e verifica por conta própria.
///         Nenhum dado descritivo, pessoal ou de conteúdo é gravado.
contract ProofAnchor {
    struct Batch {
        bytes32 root;
        uint32 leafCount;
        uint64 timestamp;
        address submitter;
    }

    Batch[] private _batches;
    mapping(address => bool) public submitters;
    address public admin;

    event BatchAnchored(
        uint256 indexed batchId, bytes32 indexed root, uint32 leafCount, address indexed submitter, uint64 timestamp
    );

    constructor() {
        admin = msg.sender;
        submitters[msg.sender] = true;
    }

    function setSubmitter(address a, bool ok) external {
        require(msg.sender == admin, "PA: apenas admin");
        submitters[a] = ok;
    }

    function anchorBatch(bytes32 root, uint32 leafCount) external returns (uint256 batchId) {
        require(submitters[msg.sender], "PA: sem permissao");
        require(root != bytes32(0) && leafCount > 0, "PA: lote invalido");
        _batches.push(Batch({root: root, leafCount: leafCount, timestamp: uint64(block.timestamp), submitter: msg.sender}));
        batchId = _batches.length - 1;
        emit BatchAnchored(batchId, root, leafCount, msg.sender, uint64(block.timestamp));
    }

    /// @notice Verifica caminho de inclusão (pares ordenados) contra a raiz do lote.
    function verifyInclusion(uint256 batchId, bytes32 leaf, bytes32[] calldata proof) external view returns (bool) {
        require(batchId < _batches.length, "PA: lote inexistente");
        bytes32 h = leaf;
        for (uint256 i = 0; i < proof.length; i++) {
            bytes32 p = proof[i];
            h = h <= p ? keccak256(abi.encodePacked(h, p)) : keccak256(abi.encodePacked(p, h));
        }
        return h == _batches[batchId].root;
    }

    function getBatch(uint256 batchId) external view returns (Batch memory) {
        require(batchId < _batches.length, "PA: lote inexistente");
        return _batches[batchId];
    }

    function batchCount() external view returns (uint256) {
        return _batches.length;
    }
}
