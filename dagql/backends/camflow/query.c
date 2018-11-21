#include "include/camquery.h"

#define MAX_NODE_STR_LEN 8192
#define NAMESPACE "dagql: "

static char from_node_str[MAX_NODE_STR_LEN];
static char to_node_str[MAX_NODE_STR_LEN];

static void init(void) {
  // Indicate the start of a graph.
  // Useful if multiple query outputs are in the message buffer.
  print(NAMESPACE "#start");
}

static void node2jsonstr(prov_entry_t* const node, char* const out_str) {
  int status;
  if (prov_type(node) == ENT_PATH) {
    status = snprintf(out_str, MAX_NODE_STR_LEN,
                      "{"
                        "\"id\": %llu, "
                        "\"type\": \"%s\", "
                        "\"machine_id\": %u, "
                        "\"boot_id\": %u, "
                        "\"path\": \"%.*s\""
                      "}",
                      node_identifier(node).id,
                      node_str(prov_type(node)),
                      node_identifier(node).machine_id,
                      node_identifier(node).boot_id,
                      (int)node->file_name_info.length,
                      node->file_name_info.name);
  } else if(prov_type(node) == ENT_INODE_DIRECTORY ||
            prov_type(node) == ENT_INODE_FILE) {
    status = snprintf(out_str, MAX_NODE_STR_LEN,
                      "{"
                        "\"id\": %llu, "
                        "\"type\": \"%s\", "
                        "\"machine_id\": %u, "
                        "\"boot_id\": %u, "
                        "\"inode\": %llu, "
                        "\"mode\": %d"
                      "}",
                      node_identifier(node).id,
                      node_str(prov_type(node)),
                      node_identifier(node).machine_id,
                      node_identifier(node).boot_id,
                      node->inode_info.ino,
                      node->inode_info.mode);
  } else {
    status = snprintf(out_str, MAX_NODE_STR_LEN,
                      "{"
                        "\"id\": %llu, "
                        "\"type\": \"%s\", "
                        "\"machine_id\": %u, "
                        "\"boot_id\": %u"
                      "}",
                      node_identifier(node).id,
                      node_str(prov_type(node)),
                      node_identifier(node).machine_id,
                      node_identifier(node).boot_id);
  }

  if (status >= MAX_NODE_STR_LEN || status < 0) {
    // something went wrong, serialize to an "error" value instead
    snprintf("null", MAX_NODE_STR_LEN, out_str);
  }
}

static int prov_flow(prov_entry_t* from, prov_entry_t* edge, prov_entry_t* to) {
  // only support a subset of possible nodes...
  if ((prov_type(from) == ENT_INODE_FILE ||
       prov_type(from) == ENT_PATH ||
       prov_type(from) == ENT_INODE_DIRECTORY ||
       prov_type(to) == ENT_INODE_FILE ||
       prov_type(to) == ENT_PATH ||
       prov_type(to) == ENT_INODE_DIRECTORY) &&
      (prov_type(edge) == RL_READ ||
       prov_type(edge) == RL_WRITE)) {
    node2jsonstr(from, from_node_str);
    node2jsonstr(to, to_node_str);
    print(NAMESPACE
          "["
            "%s, "
            "{"
              "\"id\": %llu, "
              "\"machine_id\": %u, "
              "\"boot_id\": %u, "
              "\"type\": \"%s\", "
              "\"allowed\": %d"
            "}, "
            "%s"
          "]",

          from_node_str,

          relation_identifier(edge).id,
          relation_identifier(edge).machine_id,
          relation_identifier(edge).boot_id,
          relation_str(prov_type(edge)),
          edge->relation_info.allowed,

          to_node_str);
  }

  return 0;
}

struct provenance_query_hooks hooks = {
  .flow=&prov_flow,
  .free=NULL,
  .alloc=NULL,
};

QUERY_DESCRIPTION("Log nodes and edges in JSON format");
QUERY_LICSENSE("GPL");
QUERY_AUTHOR("Jerry Yin");
QUERY_VERSION("0.1");
QUERY_NAME("provenance2json");

register_query(init, hooks);
