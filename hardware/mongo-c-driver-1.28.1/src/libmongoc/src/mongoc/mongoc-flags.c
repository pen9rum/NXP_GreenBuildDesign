/*
 * Copyright 2009-present MongoDB, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "mongoc-flags.h"

#include "mongoc-compression-private.h"
#include "mongoc-flags-private.h"

#include "mcd-rpc.h"

#include <bson/bson.h>

// Document and ensure consistency between equivalent macros in mcd-rpc and
// libmongoc.

BSON_STATIC_ASSERT (MONGOC_OP_COMPRESSED_COMPRESSOR_ID_NOOP == MONGOC_COMPRESSOR_NOOP_ID);
BSON_STATIC_ASSERT (MONGOC_OP_COMPRESSED_COMPRESSOR_ID_SNAPPY == MONGOC_COMPRESSOR_SNAPPY_ID);
BSON_STATIC_ASSERT (MONGOC_OP_COMPRESSED_COMPRESSOR_ID_ZLIB == MONGOC_COMPRESSOR_ZLIB_ID);
BSON_STATIC_ASSERT (MONGOC_OP_COMPRESSED_COMPRESSOR_ID_ZSTD == MONGOC_COMPRESSOR_ZSTD_ID);

BSON_STATIC_ASSERT (MONGOC_OP_MSG_FLAG_NONE == MONGOC_MSG_NONE);
BSON_STATIC_ASSERT (MONGOC_OP_MSG_FLAG_CHECKSUM_PRESENT == MONGOC_MSG_CHECKSUM_PRESENT);
BSON_STATIC_ASSERT (MONGOC_OP_MSG_FLAG_MORE_TO_COME == MONGOC_MSG_MORE_TO_COME);
BSON_STATIC_ASSERT (MONGOC_OP_MSG_FLAG_EXHAUST_ALLOWED == MONGOC_MSG_EXHAUST_ALLOWED);

BSON_STATIC_ASSERT (MONGOC_OP_REPLY_RESPONSE_FLAG_NONE == MONGOC_REPLY_NONE);
BSON_STATIC_ASSERT (MONGOC_OP_REPLY_RESPONSE_FLAG_CURSOR_NOT_FOUND == MONGOC_REPLY_CURSOR_NOT_FOUND);
BSON_STATIC_ASSERT (MONGOC_OP_REPLY_RESPONSE_FLAG_QUERY_FAILURE == MONGOC_REPLY_QUERY_FAILURE);
BSON_STATIC_ASSERT (MONGOC_OP_REPLY_RESPONSE_FLAG_SHARD_CONFIG_STALE == MONGOC_REPLY_SHARD_CONFIG_STALE);
BSON_STATIC_ASSERT (MONGOC_OP_REPLY_RESPONSE_FLAG_AWAIT_CAPABLE == MONGOC_REPLY_AWAIT_CAPABLE);

BSON_STATIC_ASSERT (MONGOC_OP_UPDATE_FLAG_NONE == MONGOC_UPDATE_NONE);
BSON_STATIC_ASSERT (MONGOC_OP_UPDATE_FLAG_UPSERT == MONGOC_UPDATE_UPSERT);
BSON_STATIC_ASSERT (MONGOC_OP_UPDATE_FLAG_MULTI_UPDATE == MONGOC_UPDATE_MULTI_UPDATE);

BSON_STATIC_ASSERT (MONGOC_OP_INSERT_FLAG_NONE == MONGOC_INSERT_NONE);
BSON_STATIC_ASSERT (MONGOC_OP_INSERT_FLAG_CONTINUE_ON_ERROR == MONGOC_INSERT_CONTINUE_ON_ERROR);

BSON_STATIC_ASSERT (MONGOC_OP_QUERY_FLAG_NONE == MONGOC_QUERY_NONE);
BSON_STATIC_ASSERT (MONGOC_OP_QUERY_FLAG_TAILABLE_CURSOR == MONGOC_QUERY_TAILABLE_CURSOR);
BSON_STATIC_ASSERT (MONGOC_OP_QUERY_FLAG_SECONDARY_OK == MONGOC_QUERY_SECONDARY_OK);
BSON_STATIC_ASSERT (MONGOC_OP_QUERY_FLAG_OPLOG_REPLAY == MONGOC_QUERY_OPLOG_REPLAY);
BSON_STATIC_ASSERT (MONGOC_OP_QUERY_FLAG_NO_CURSOR_TIMEOUT == MONGOC_QUERY_NO_CURSOR_TIMEOUT);
BSON_STATIC_ASSERT (MONGOC_OP_QUERY_FLAG_AWAIT_DATA == MONGOC_QUERY_AWAIT_DATA);
BSON_STATIC_ASSERT (MONGOC_OP_QUERY_FLAG_EXHAUST == MONGOC_QUERY_EXHAUST);
BSON_STATIC_ASSERT (MONGOC_OP_QUERY_FLAG_PARTIAL == MONGOC_QUERY_PARTIAL);

BSON_STATIC_ASSERT (MONGOC_OP_DELETE_FLAG_NONE == MONGOC_DELETE_NONE);
BSON_STATIC_ASSERT (MONGOC_OP_DELETE_FLAG_SINGLE_REMOVE == MONGOC_DELETE_SINGLE_REMOVE);
