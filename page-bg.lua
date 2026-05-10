local function stringify(value)
  return pandoc.utils.stringify(value)
end

local function starts_with(value, prefix)
  return value:sub(1, #prefix) == prefix
end

local function css_escape(value)
  return value:gsub("\\", "\\\\"):gsub('"', '\\"'):gsub("\n", "")
end

function Meta(meta)
  local page_bg = meta["page-bg"]
  if not page_bg then
    return meta
  end

  local bg = stringify(page_bg)
  if bg == "" then
    return meta
  end

  local href = bg
  if not (
    starts_with(bg, "http://") or
    starts_with(bg, "https://") or
    starts_with(bg, "/") or
    starts_with(bg, "./") or
    starts_with(bg, "../")
  ) then
    href = "/" .. bg
  end

  local style = '<style id="page-bg-style">body{--page-bg-image:url("' .. css_escape(href) .. '");}</style>'
  local block = pandoc.RawBlock("html", style)
  local header = meta["header-includes"]

  if not header then
    meta["header-includes"] = pandoc.MetaBlocks({ block })
  elseif header.t == "MetaBlocks" then
    table.insert(header, block)
    meta["header-includes"] = header
  else
    meta["header-includes"] = pandoc.MetaList({ header, pandoc.MetaBlocks({ block }) })
  end

  return meta
end
